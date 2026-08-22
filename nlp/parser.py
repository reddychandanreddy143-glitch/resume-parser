import os
import re
import sys
from pathlib import Path

# Ensure root directory is accessible
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from extractors.text_extractor import extract_resume_text
from nlp.cleaner import clean_text
from nlp.patterns import extract_email, extract_phone
from nlp.name_extractor import extract_name
from nlp.skills_extractor import extract_skills

# Standard section header markers
SECTION_HEADERS = {
    "education": ["education", "academic background", "academics", "qualifications"],
    "experience": ["experience", "work experience", "employment history", "internships"],
    "projects": ["projects", "personal projects", "academic projects"],
    "certifications": ["certifications", "certificates", "licenses"]
}

def segment_sections(text: str) -> dict[str, str]:
    """
    Splits resume text into recognized functional sections.
    """
    lines = text.splitlines()
    sections = {}
    current_section = "general"
    sections[current_section] = []

    for line in lines:
        cleaned_line = line.strip().lower()
        # Remove markdown/bullet markers for header check
        header_candidate = re.sub(r"^[-*#•\s]+", "", cleaned_line)

        matched_section = None
        for sec_name, keywords in SECTION_HEADERS.items():
            if header_candidate in keywords:
                matched_section = sec_name
                break

        if matched_section:
            current_section = matched_section
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections[current_section].append(line)

    return {sec: "\n".join(content).strip() for sec, content in sections.items() if content}

def parse_resume(file_path: str) -> dict:
    """
    Master pipeline: Reads a document, normalizes text, and extracts
    structured candidate profile data.
    """
    # 1. Extract raw text
    raw_text = extract_resume_text(file_path)

    # 2. Clean and normalize
    cleaned = clean_text(raw_text)

    # 3. Segment sections
    sections = segment_sections(cleaned)

    # 4. Extract entities
    name = extract_name(cleaned)
    email = extract_email(cleaned)
    phone = extract_phone(cleaned)
    skills = extract_skills(cleaned)

    return {
        "candidate_name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "sections": {
            "education": sections.get("education", ""),
            "experience": sections.get("experience", ""),
            "projects": sections.get("projects", "")
        }
    }

if __name__ == "__main__":
    test_file = "sample_resume.pdf"
    if os.path.exists(test_file):
        import json
        print("=== RUNNING MASTER RESUME PARSER ===")
        profile = parse_resume(test_file)
        print(json.dumps(profile, indent=2))