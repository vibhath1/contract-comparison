from app.core.document_processor import extract_text
from app.core.comparison_engine import compare_documents
from app.core.report_generator import generate_html_report

def test_html_report():
    file1 = "uploads/4f323908-de5a-4d9c-92bd-58a5922dc74d.pdf"
    file2 = "uploads/86d5bf96-9324-4712-9cd3-df6f90eb4434.docx"

    # Extract text
    text1 = extract_text(file1)
    text2 = extract_text(file2)

    # Compare
    result = compare_documents(text1, text2, file1, file2)

    # Generate report
    report_file = generate_html_report(result, "comparison_report.html")
    print(f"✅ Report saved to: {report_file}")

if __name__ == "__main__":
    test_html_report()
