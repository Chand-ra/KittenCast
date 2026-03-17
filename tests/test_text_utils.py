import pytest
from unittest.mock import patch, mock_open
from kittencast.text_utils import (
    split_text, 
    extract_document,
    extract_text_from_txt
)

# --- 1. Text Splitting (Chunking) Tests ---

def test_split_text_standard():
    """Test that text splits correctly at sentence boundaries."""
    text = "This is the first sentence. This is the second sentence."
    chunks = split_text(text, max_chars=35)
    
    assert len(chunks) == 2
    assert chunks[0] == "This is the first sentence."
    assert chunks[1] == "This is the second sentence."

def test_split_text_preserves_long_sentences():
    """Test that it doesn't arbitrarily chop a sentence that exceeds max_chars."""
    long_sentence = "This is a very long sentence " + ("a" * 400) + "."
    chunks = split_text(long_sentence, max_chars=400)
    
    assert len(chunks) == 1
    assert chunks[0] == long_sentence

def test_split_text_groups_short_sentences():
    """Test that multiple short sentences are grouped into a single chunk to maximize TTS efficiency."""
    text = "Hi. Hello. How are you? I am fine."
    # "Hi. Hello." = 10 chars. Adding "How are you?" pushes it over 15.
    chunks = split_text(text, max_chars=15)
    
    assert len(chunks) == 3
    assert chunks[0] == "Hi. Hello."
    assert chunks[1] == "How are you?"
    assert chunks[2] == "I am fine."

def test_split_text_empty():
    """Test behavior with empty string input."""
    assert split_text("") == []


# --- 2. Document Router & Extraction Tests ---

def test_extract_document_unsupported_type():
    """Test that the router strictly rejects unsupported file extensions."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_document("my_book.mobi")

@patch('kittencast.text_utils.extract_text_from_txt')
def test_extract_document_routes_txt(mock_extract):
    """Test that .txt files are routed to the correct extractor."""
    mock_extract.return_value = ["Dummy text content"]
    result = extract_document("document.txt")
    
    mock_extract.assert_called_once_with("document.txt")
    assert result == ["Dummy text content"]

@patch('kittencast.text_utils.extract_text_from_pdf')
def test_extract_document_routes_pdf(mock_extract):
    """Test that .pdf files are routed to the correct extractor."""
    mock_extract.return_value = ["Dummy pdf content"]
    extract_document("paper.pdf")
    
    mock_extract.assert_called_once_with("paper.pdf")

@patch('kittencast.text_utils.extract_text_from_epub')
def test_extract_document_routes_epub(mock_extract):
    """Test that .epub files are routed to the correct extractor."""
    mock_extract.return_value = ["Dummy epub content"]
    extract_document("book.epub")
    
    mock_extract.assert_called_once_with("book.epub")

@patch('kittencast.text_utils.extract_text_from_docx')
def test_extract_document_routes_docx(mock_extract):
    """Test that .docx files are routed to the correct extractor."""
    mock_extract.return_value = ["Dummy docx content"]
    extract_document("notes.docx")
    
    mock_extract.assert_called_once_with("notes.docx")

def test_actual_txt_extraction_logic():
    """Test the actual file reading logic for a text file using a mocked file system."""
    mock_file_content = "This is a test file.\nIt has two lines."
    
    # We mock Python's built-in `open` function so it reads our string instead of looking for a file
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        result = extract_text_from_txt("fake_path.txt")
        assert result == [mock_file_content]