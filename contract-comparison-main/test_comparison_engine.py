from app.core.document_processor import extract_text
from app.core.comparison_engine import compare_documents
import sys

def test_comparison(file1_path, file2_path):
    print(f"\nExtracting from: {file1_path}")
    text1 = extract_text(file1_path)

    print(f"\nExtracting from: {file2_path}")
    text2 = extract_text(file2_path)

    print("\n🔍 Comparing documents...")
    results = compare_documents(text1, text2)

    print("\n🧾 Text Differences (Unified Diff):")
    print(results["text_diff"][:1000])  # Show first 1000 chars

    print("\n📘 Grammar Issues in Document 1:")
    for issue in results["grammar_issues_doc1"][:5]:  # limit output
        print(f"- {issue['message']} | Suggestions: {issue['suggestions']}")

    print("\n📙 Grammar Issues in Document 2:")
    for issue in results["grammar_issues_doc2"][:5]:
        print(f"- {issue['message']} | Suggestions: {issue['suggestions']}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_comparison_engine.py file1 file2")
    else:
        test_comparison(sys.argv[1], sys.argv[2])
