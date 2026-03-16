import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize

# Ensure tokenizer is available globally for the module
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

def extract_chapters(epub_path: str) -> list[str]:
    book = epub.read_epub(epub_path)
    chapters = []
    
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        text = ' '.join([para.get_text() for para in soup.find_all('p')]).strip()
        if len(text) > 150:
            chapters.append(text)
    return chapters

def split_text(text: str, max_chars: int = 400) -> list[str]:
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
            
    if current_chunk:
         chunks.append(current_chunk.strip())
    return chunks