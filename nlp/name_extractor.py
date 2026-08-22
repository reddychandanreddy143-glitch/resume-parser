import re
import spacy

# Load the lightweight English NLP model
nlp = spacy.load("en_core_web_sm")

# Words that should never be considered part of a candidate's name
BLACKLISTED_WORDS = {
    "resume", "curriculum", "vitae", "cv", "page", "email", "phone", 
    "contact", "profile", "summary", "experience", "education", 
    "skills", "projects", "developer", "engineer", "designer", "manager"
}

def extract_name(text: str) -> str | None:
    """
    Extracts candidate name using a hybrid approach of spaCy NER 
    and positional heuristics.
    
    Args:
        text (str): Cleaned resume text.
        
    Returns:
        str | None: Detected candidate name or None.
    """
    if not text:
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # 1. Inspect top 5 lines where candidate names are standardly located
    header_lines = lines[:5]
    header_text = "\n".join(header_lines)

    doc = nlp(header_text)

    # Strategy A: spaCy PERSON entity detection
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            cleaned_entity = ent.text.strip()
            tokens = cleaned_entity.lower().split()
            # Verify no blacklisted terms are present
            if not any(token in BLACKLISTED_WORDS for token in tokens):
                # Valid name should be between 2 and 4 words
                if 1 <= len(tokens) <= 4:
                    return cleaned_entity

    # Strategy B: Fallback heuristic — scan first non-blacklisted capitalized line
    for line in header_lines:
        # Skip lines with contact information or symbols
        if "@" in line or any(char in line for char in [":", "|", "/", "\\", "+"]):
            continue
        
        words = line.split()
        lower_words = [w.lower() for w in words]
        
        # Check if line looks like a title/name (1-4 words, starts with uppercase, no blacklisted words)
        if 1 <= len(words) <= 4:
            if not any(w in BLACKLISTED_WORDS for w in lower_words):
                if all(w[0].isupper() for w in words if w.isalpha()):
                    return line

    return None


if __name__ == "__main__":
    test_resumes = [
        "Chandan Reddy\nEmail: chandan.reddy@example.com | Phone: 9876543210\nSoftware Developer",
        "CURRICULUM VITAE\nAshwini Kumar\nPhone: +91 9123456780",
        "Email: test@example.com\nReddy Chandan\nEducation: BCA"
    ]
    
    print("=== TESTING NAME EXTRACTION ===")
    for resume in test_resumes:
        name = extract_name(resume)
        print(f"Resume Snippet:\n{resume}\n-> Detected Name: {name}\n")