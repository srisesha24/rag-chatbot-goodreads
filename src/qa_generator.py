import json
import csv
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

class QAGenerator:
    def __init__(self, qa_output_dir="data/processed"):
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            print("ERROR: GROQ_API_KEY not found in .env file!")
            print(f"Current directory: {os.getcwd()}")
            sys.exit(1)
        
        print(f"Using API key: {api_key[:20]}...")
        self.client = Groq(api_key=api_key)
        self.qa_output_dir = Path(qa_output_dir)
        self.qa_output_dir.mkdir(parents=True, exist_ok=True)
        self.qa_pairs = []
    
    def generate_qa_from_book(self, book_data: dict, num_questions=2):
        """Generate Q/A pairs from a single book"""
        
        context = f"""
        Title: {book_data.get('title', 'Unknown')}
        Author: {book_data.get('author', 'Unknown')}
        Rating: {book_data.get('rating', 'N/A')}/5
        """
        
        prompt = f"""Based on this self-help book, generate {num_questions} realistic Q&A pairs.

Book Info:
{context}

Format as JSON array ONLY (no other text):
[
    {{"question": "...", "answer": "..."}},
    {{"question": "...", "answer": "..."}}
]
"""
        
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=1,
                max_tokens=500,
            )
            
            response_text = completion.choices[0].message.content.strip()
            qa_list = json.loads(response_text)
            
            for qa in qa_list:
                qa['source_book'] = book_data.get('title', 'Unknown')
                qa['source_author'] = book_data.get('author', 'Unknown')
            
            self.qa_pairs.extend(qa_list)
            print(f"✓ Generated {len(qa_list)} Q/A pairs for: {book_data.get('title')}")
            return qa_list
            
        except Exception as e:
            print(f"Error for {book_data.get('title')}: {e}")
            return []
    
    def generate_qa_from_file(self, books_file: str, books_to_process: int = None):
        """Generate Q/A from all books"""
        
        with open(books_file, 'r', encoding='utf-8') as f:
            books = json.load(f)
        
        if books_to_process:
            books = books[:books_to_process]
        
        print(f"Processing {len(books)} books...\n")
        
        for idx, book in enumerate(books):
            print(f"[{idx+1}/{len(books)}] {book.get('title')}")
            self.generate_qa_from_book(book, num_questions=2)
        
        print(f"\nTotal Q/A pairs: {len(self.qa_pairs)}")
    
    def save_qa_dataset(self):
        """Save as CSV"""
        filename = self.qa_output_dir / 'qa_dataset.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['question', 'answer', 'source_book', 'source_author'])
            writer.writeheader()
            writer.writerows(self.qa_pairs)
        
        print(f"Saved to {filename}")

if __name__ == "__main__":
    qa_gen = QAGenerator()
    qa_gen.generate_qa_from_file('data/raw/goodreads_books.json', books_to_process=15)
    qa_gen.save_qa_dataset()
