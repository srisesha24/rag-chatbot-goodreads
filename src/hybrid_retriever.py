import json
import csv
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

class HybridRetriever:
    def __init__(self, vector_db_path="data/chroma_db"):
        self.vector_db_path = vector_db_path
        self.client = chromadb.PersistentClient(path=vector_db_path)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_collection = None
        self.qa_pairs = []
        self.qa_embeddings = None
    
    def load_qa_dataset(self, qa_file: str):
        """Load Q/A dataset"""
        with open(qa_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.qa_pairs = list(reader)
        
        questions = [qa['question'] for qa in self.qa_pairs]
        print(f"Encoding {len(questions)} questions...")
        self.qa_embeddings = self.embedding_model.encode(questions, convert_to_numpy=True)
        print(f"✓ Loaded {len(self.qa_pairs)} Q/A pairs")
    
    def create_qa_collection(self):
        """Create Chroma collection"""
        self.qa_collection = self.client.get_or_create_collection(
            name="qa_pairs",
            metadata={"hnsw:space": "cosine"}
        )
        
        for idx, qa in enumerate(self.qa_pairs):
            self.qa_collection.add(
                ids=[f"qa_{idx}"],
                documents=[qa['question']],
                metadatas=[{
                    'answer': qa['answer'],
                    'source_book': qa.get('source_book', 'Unknown'),
                }],
                embeddings=[self.qa_embeddings[idx].tolist()]
            )
        
        print(f"✓ Created Q/A collection with {len(self.qa_pairs)} pairs")
    
    def hybrid_search(self, query: str, top_k: int = 1):
        """Search Q/A pairs"""
        query_embedding = self.embedding_model.encode(query, convert_to_numpy=True)
        similarities = np.dot(self.qa_embeddings, query_embedding) / (
            np.linalg.norm(self.qa_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8
        )
        
        top_idx = np.argsort(similarities)[::-1][0]
        qa = self.qa_pairs[int(top_idx)]
        score = float(similarities[top_idx])
        
        return {
            'question': qa['question'],
            'answer': qa['answer'],
            'source_book': qa.get('source_book', 'Unknown'),
            'confidence': score
        }

if __name__ == "__main__":
    print("Building vector database...")
    retriever = HybridRetriever()
    retriever.load_qa_dataset('data/processed/qa_dataset.csv')
    retriever.create_qa_collection()
    print("\n✓ Vector database ready!")
