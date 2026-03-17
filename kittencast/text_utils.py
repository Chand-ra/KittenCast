import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
import pypdf
import docx

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

def extract_text_from_epub(file_path: str) -> list[str]:
    book = epub.read_epub(file_path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        text = ' '.join([para.get_text() for para in soup.find_all('p')]).strip()
        if len(text) > 150:
            chapters.append(text)
    return chapters

def extract_text_from_pdf(file_path: str) -> list[str]:
    pages = []
    with open(file_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text and len(text.strip()) > 150:
                pages.append(text.strip())
    return pages

def extract_text_from_docx(file_path: str) -> list[str]:
    doc = docx.Document(file_path)
    # Join all paragraphs into one giant string. 
    # Our split_text function will handle chunking it safely later.
    full_text = ' '.join([para.text for para in doc.paragraphs if para.text.strip()])
    return [full_text] if full_text else []

def extract_text_from_txt(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    return [text] if text else []

def extract_document(file_path: str) -> list[str]:
    """Routes the file to the correct extractor based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.epub':
        return extract_text_from_epub(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: '{ext}'. Supported types are .epub, .pdf, .docx, .txt")

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