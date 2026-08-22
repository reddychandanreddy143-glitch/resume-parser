from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Candidate Name
pdf.set_font("Helvetica", style="B", size=18)
pdf.cell(0, 10, text="Chandan Reddy", new_x="LMARGIN", new_y="NEXT")

# Contact Information
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 6, text="Email: chandan.reddy@example.com | Phone: +91 9876543210", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)

# Technical Skills
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(0, 8, text="TECHNICAL SKILLS", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, text="Python, Java, SQL, Flask, Git, PostgreSQL, NLP, Machine Learning")
pdf.ln(4)

# Education
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(0, 8, text="EDUCATION", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 6, text="Bachelor of Computer Applications (BCA)", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, text="Bengaluru North University (2023 - 2026)", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)

# Experience
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(0, 8, text="EXPERIENCE", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 6, text="Python Developer Intern - Codec Technologies", new_x="LMARGIN", new_y="NEXT")
pdf.multi_cell(0, 6, text="- Built NLP text processing pipelines and Flask REST APIs.")
pdf.ln(4)

# Projects
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(0, 8, text="PROJECTS", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, text="Automated Resume Parser: ATS document processing system using Python and Flask.")

# Output PDF
pdf.output("sample_resume.pdf")
print("sample_resume.pdf created successfully!")