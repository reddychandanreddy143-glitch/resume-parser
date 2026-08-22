import re

# Comprehensive email regex pattern matching standard RFC-compliant addresses
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    re.IGNORECASE
)

# Flexible phone regex matching standard Indian & international number patterns
PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?"       # Optional country code like +91, 91, +1
    r"\(?\d{2,5}\)?[-.\s]?"          # Area code or initial digits
    r"\d{3,5}[-.\s]?\d{3,5}"         # Middle and trailing digits
)

def extract_email(text: str) -> str | None:
    """
    Extracts the primary email address from the supplied text.
    """
    if not text:
        return None

    match = EMAIL_PATTERN.search(text)
    if match:
        return match.group(0).strip().lower()
    return None


def extract_phone(text: str) -> str | None:
    """
    Extracts the primary phone number from resume text.
    Validates that extracted number contains between 10 and 13 digits.
    """
    if not text:
        return None

    matches = PHONE_PATTERN.finditer(text)
    for match in matches:
        raw_phone = match.group(0).strip()
        # Keep only numeric digits for length validation
        digits = re.sub(r"\D", "", raw_phone)
        
        # Valid phone numbers have 10 to 13 digits (excluding 4-digit years or 6-digit pin codes)
        if 10 <= len(digits) <= 13:
            return raw_phone

    return None


if __name__ == "__main__":
    sample_texts = [
        "Reach me at +91 9876543210 or email test@example.com",
        "Mobile: 9876543210 | Graduated: 2026",
        "Phone: +91-98765-43210 (Work)",
        "Call: 09876543210",
        "Pin code 560001, Year 2024 (No valid phone)"
    ]
    
    print("=== TESTING PHONE EXTRACTION ===")
    for sample in sample_texts:
        phone = extract_phone(sample)
        print(f"Text: '{sample}'\n-> Extracted Phone: {phone}\n")