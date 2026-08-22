import re
import unicodedata

def clean_text(raw_text: str) -> str:
    """
    Cleans and normalizes extracted resume text while preserving 
    critical casing, punctuation, and technical terms.
    
    Args:
        raw_text (str): Raw string extracted from document.
        
    Returns:
        str: Normalized, clean text.
    """
    if not raw_text:
        return ""

    # 1. Normalize unicode characters (converts special quotes, dashes, non-breaking spaces)
    text = unicodedata.normalize("NFKD", raw_text)

    # 2. Replace bullet points, decorative unicode symbols with standard newlines or dashes
    text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\uf0b7\u25aa\u25ab]", "\n- ", text)

    # 3. Normalize horizontal whitespace (convert multiple spaces/tabs into a single space)
    lines = []
    for line in text.splitlines():
        cleaned_line = re.sub(r"[ \t]+", " ", line).strip()
        if cleaned_line:
            lines.append(cleaned_line)

    # 4. Reconstruct clean text with consistent line breaks
    return "\n".join(lines)


if __name__ == "__main__":
    messy_sample = """
    Chandan   Reddy
    Email:   chandan.reddy@example.com \xa0 | \xa0 Phone: +91 9876543210
    
    • TECHNICAL SKILLS
       Python ,   Java,   C++ ,   Flask
    
    • EDUCATION
    BCA    -- Bengaluru   North   University
    """
    print("=== RAW MESSY TEXT ===")
    print(messy_sample)
    print("\n=== CLEANED TEXT ===")
    cleaned = clean_text(messy_sample)
    print(cleaned)