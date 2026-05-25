import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path

class GoodreadsScraper:
    def __init__(self, output_dir="data/raw"):
        self.base_url = "https://www.goodreads.com/shelf/show/self-help"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.books = []
    
    def scrape_page(self, page_num=1):
        """Scrape a single page of the Goodreads self-help shelf"""
        params = {'page': page_num}
        
        try:
            print(f"Scraping page {page_num}...")
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all book entries
            book_entries = soup.find_all('div', class_='elementList')
            
            if not book_entries:
                print(f"No books found on page {page_num}.")
                return 0
            
            for entry in book_entries:
                try:
                    title_elem = entry.find('a', class_='bookTitle')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    author_elem = entry.find('span', class_='authorName')
                    author = author_elem.get_text(strip=True) if author_elem else "N/A"
                    
                    rating_text = entry.find('span', class_='greyText smallText')
                    rating = "N/A"
                    if rating_text:
                        text = rating_text.get_text(strip=True)
                        if 'avg rating' in text:
                            rating = text.split('avg rating ')[1].split(' ')[0]
                    
                    link = title_elem['href'] if title_elem and title_elem.has_attr('href') else "N/A"
                    
                    book = {
                        'title': title,
                        'author': author,
                        'rating': rating,
                        'url': f"https://www.goodreads.com{link}" if link != "N/A" else "N/A"
                    }
                    
                    self.books.append(book)
                    print(f"  ✓ {title}")
                
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
            
            time.sleep(2)  # Be respectful to server
            return len(book_entries)
        
        except Exception as e:
            print(f"Error fetching page {page_num}: {e}")
            return 0
    
    def scrape_multiple_pages(self, num_pages=3):
        """Scrape multiple pages"""
        for page in range(1, num_pages + 1):
            count = self.scrape_page(page)
            if count == 0:
                break
        
        print(f"\nTotal books scraped: {len(self.books)}")
    
    def save_data(self):
        """Save scraped data to file"""
        filename = self.output_dir / "goodreads_books.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, indent=2, ensure_ascii=False)
        
        print(f"Saved to {filename}")

if __name__ == "__main__":
    scraper = GoodreadsScraper()
    scraper.scrape_multiple_pages(num_pages=2)  # Scrape 2 pages (about 25 books)
    scraper.save_data()
