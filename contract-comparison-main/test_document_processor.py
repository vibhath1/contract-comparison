from app.core.document_processor import extract_text
import sys

def test_extraction(file_path):
    try:
        print(f"\nExtracting text from: {file_path}")
        text = extract_text(file_path)
        print("Extracted text:")
        print(text[:1000])  # Show first 1000 characters
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_document_processor.py path/to/document")
    else:
        test_extraction(sys.argv[1])
