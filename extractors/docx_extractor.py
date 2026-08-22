import os
from docx import Document

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from paragraphs and tables in a .docx file using python-docx.
    
    Args:
        file_path (str): Path to the .docx document.
        
    Returns:
        str: Extracted plain text content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DOCX file not found at: {file_path}")

    doc = Document(file_path)
    extracted_text = []

    # 1. Extract text from standard paragraphs
    for paragraph in doc.paragraphs:
        cleaned_line = paragraph.text.strip()
        if cleaned_line:
            extracted_text.append(cleaned_line)

    # 2. Extract text from any tables inside the document
    for table in doc.tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if row_data:
                extracted_text.append(" | ".join(row_data))

    return "\n".join(extracted_text).strip()


if __name__ == "__main__":
    test_docx_path = "sample_resume.docx"
    if os.path.exists(test_docx_path):
        print("=== EXTRACTED DOCX TEXT ===")
        content = extract_text_from_docx(test_docx_path)
        print(content)
        print("===========================")
        print(f"Total characters extracted: {len(content)}")
    else:
        print(f"Could not find test file: {test_docx_path}")