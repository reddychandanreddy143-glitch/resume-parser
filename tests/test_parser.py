import os
import sys
import unittest
from pathlib import Path

# Ensure root directory is on the path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from nlp.patterns import extract_email, extract_phone
from nlp.skills_extractor import extract_skills
from nlp.name_extractor import extract_name
from nlp.parser import parse_resume

class TestResumeParser(unittest.TestCase):

    def test_email_extraction(self):
        sample = "Contact candidate at test.developer@domain.com for inquiries."
        email = extract_email(sample)
        self.assertEqual(email, "test.developer@domain.com")

    def test_phone_extraction(self):
        sample = "Call me at +91 9876543210 or 080-123456."
        phone = extract_phone(sample)
        self.assertIsNotNone(phone)
        self.assertIn("9876543210", phone)

    def test_skills_extraction(self):
        sample = "Technical toolkit: Python, Flask, PostgreSQL, Docker, and Git."
        skills = extract_skills(sample)
        self.assertIn("programming_languages", skills)
        self.assertIn("Python", skills["programming_languages"])
        self.assertIn("Flask", skills["web_frameworks"])
        self.assertIn("PostgreSQL", skills["databases"])

    def test_name_extraction(self):
        sample = "Chandan Reddy\nchandan@example.com\nPython Developer"
        name = extract_name(sample)
        self.assertEqual(name, "Chandan Reddy")

    def test_end_to_end_pdf_parser(self):
        pdf_path = os.path.join(ROOT_DIR, "sample_resume.pdf")
        if os.path.exists(pdf_path):
            result = parse_resume(pdf_path)
            self.assertEqual(result["candidate_name"], "Chandan Reddy")
            self.assertEqual(result["email"], "chandan.reddy@example.com")
            self.assertTrue(len(result["skills"]) > 0)

if __name__ == "__main__":
    unittest.main()