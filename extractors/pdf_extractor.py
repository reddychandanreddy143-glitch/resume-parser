import os
import pdfplumber

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from all pages of a given PDF file using pdfplumber.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: Extracted plain text content from the PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    extracted_pages = []

    # Open PDF safely using a context manager
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                extracted_pages.append(text)

    # Join pages separated by newlines
    full_text = "\n".join(extracted_pages).strip()
    return full_text


if __name__ == "__main__":
    test_pdf_path = "sample_resume.pdf"
    if os.path.exists(test_pdf_path):
        print("=== EXTRACTED PDF TEXT ===")
        content = extract_text_from_pdf(test_pdf_path)
        print(content)
        print("==========================")
        print(f"Total characters extracted: {len(content)}")
    else:
        print(f"Could not find test file: {test_pdf_path}")