import os
import sys
from pathlib import Path

# Ensure root directory is in sys.path so imports work from anywhere
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from extractors.pdf_extractor import extract_text_from_pdf
from extractors.docx_extractor import extract_text_from_docx

def extract_resume_text(file_path: str) -> str:
    """
    Unified text extraction router. Detects file type and invokes 
    the appropriate document extractor.
    
    Args:
        file_path (str): Path to the resume file (.pdf or .docx).
        
    Returns:
        str: Extracted plain text content.
        
    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the file extension is unsupported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: '{extension}'. Only .pdf and .docx are supported.")


if __name__ == "__main__":
    for sample_file in ["sample_resume.pdf", "sample_resume.docx"]:
        if os.path.exists(sample_file):
            print(f"=== TESTING ROUTER WITH: {sample_file} ===")
            text = extract_resume_text(sample_file)
            print(text[:120] + "...")
            print(f"Extraction successful ({len(text)} chars)\n")
        else:
            print(f"Sample not found: {sample_file}")