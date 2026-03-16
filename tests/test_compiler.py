from kittencast.text_utils import split_text

def test_split_text_respects_max_chars():
    sample_text = "This is the first sentence. This is the second sentence. And a third."
    
    # Force a very small chunk size to test the split
    chunks = split_text(sample_text, max_chars=30)
    
    assert len(chunks) > 1
    assert "This is the first sentence." in chunks[0]
    
def test_split_text_handles_empty_string():
    chunks = split_text("", max_chars=400)
    assert len(chunks) == 0