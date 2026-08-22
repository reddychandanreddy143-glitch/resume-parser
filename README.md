# AI Resume Parser & ATS Engine

An end-to-end Automated Resume Parser and Applicant Tracking System (ATS) engine built with Python, Flask, spaCy, and SQLite.

---

## Features
- **Multi-Format Extraction**: Supports both PDF (`pdfplumber`) and DOCX (`python-docx`).
- **Entity Extraction**:
  - **Candidate Name**: spaCy NER with positional heuristics.
  - **Email & Phone**: RFC-compliant regex patterns and Indian/international mobile formats.
  - **Categorized Skills**: JSON-backed taxonomy covering programming languages, frameworks, databases, and DevOps.
- **Section Segmentation**: Identifies and separates Education, Experience, and Projects.
- **RESTful API**: Endpoints for resume uploading (`/api/parse`) and record retrieval (`/api/resumes`).
- **Relational Storage**: SQLite with SQLAlchemy ORM.
- **Interactive UI**: Responsive Bootstrap 5 dashboard.

---

## Project Structure