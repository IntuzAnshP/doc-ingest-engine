import pytest
from doc_ingest.normalizer.cleaner import ContentCleaner

def test_cleaner_soft_wrap():
    cleaner = ContentCleaner()
    text = "This is a devic\ne that runs smoothly."
    cleaned = cleaner.clean(text)
    assert "device that runs" in cleaned

def test_cleaner_excessive_whitespace():
    cleaner = ContentCleaner()
    text = "Hello    world!\n\n\n\n\nNew paragraph."
    cleaned = cleaner.clean(text)
    assert cleaned == "Hello world!\n\nNew paragraph."

def test_cleaner_control_characters():
    cleaner = ContentCleaner()
    text = "Text with \x00 null byte and \x07 bell."
    cleaned = cleaner.clean(text)
    assert cleaned == "Text with null byte and bell."
