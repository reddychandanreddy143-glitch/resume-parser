import json
import os
import re
from pathlib import Path

# Locate skills database
ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DB_PATH = ROOT_DIR / "data" / "skills.json"

def load_skills_database() -> dict[str, list[str]]:
    """Loads technical skills taxonomy from JSON."""
    if not os.path.exists(SKILLS_DB_PATH):
        raise FileNotFoundError(f"Skills database not found at: {SKILLS_DB_PATH}")
    with open(SKILLS_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_skills(text: str) -> dict[str, list[str]]:
    """
    Extracts categorized skills from resume text using boundary-safe matching.
    
    Args:
        text (str): Cleaned resume text.
        
    Returns:
        dict: Grouped skills found in the document.
    """
    if not text:
        return {}

    skills_data = load_skills_database()
    matched_skills = {}

    for category, skill_list in skills_data.items():
        found = []
        for skill in skill_list:
            # Handle special characters like C++, .NET, C# safely in regex
            escaped_skill = re.escape(skill)
            
            # Use word boundaries (\b) or delimiter checks
            if skill in ["C++", "C#", ".NET"]:
                pattern = rf"(?:^|[\s,;/|]){escaped_skill}(?:$|[\s,;/|])"
            else:
                pattern = rf"\b{escaped_skill}\b"

            if re.search(pattern, text, re.IGNORECASE):
                found.append(skill)

        if found:
            matched_skills[category] = sorted(list(set(found)))

    return matched_skills


if __name__ == "__main__":
    sample_text = """
    Chandan Reddy
    Skills: Python, C++, Java, Flask, PostgreSQL, Docker, Git, and Natural Language Processing (NLP).
    Experienced in React, HTML, CSS, and machine learning.
    """
    
    print("=== TESTING SKILLS EXTRACTION ===")
    results = extract_skills(sample_text)
    for category, items in results.items():
        print(f"[{category}]: {', '.join(items)}")