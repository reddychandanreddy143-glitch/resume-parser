import json
import os
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

import config
from database import SessionLocal, init_db, ResumeRecord, save_parsed_resume
from nlp.parser import parse_resume

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

init_db()

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/parse", methods=["POST"])
def upload_and_parse():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file provided in request."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        try:
            parsed_data = parse_resume(save_path)
            record_id = save_parsed_resume(filename, parsed_data)
            return jsonify({
                "message": "Resume parsed and saved successfully.",
                "candidate_id": record_id,
                "data": parsed_data
            }), 201
        except Exception as e:
            return jsonify({"error": f"Failed to process resume: {str(e)}"}), 500

    return jsonify({"error": "Invalid file format. Only .pdf and .docx are supported."}), 400

@app.route("/api/resumes", methods=["GET"])
def get_all_resumes():
    session = SessionLocal()
    try:
        records = session.query(ResumeRecord).order_by(ResumeRecord.id.desc()).all()
        results = []
        for r in records:
            results.append({
                "id": r.id,
                "filename": r.filename,
                "candidate_name": r.candidate_name,
                "email": r.email,
                "phone": r.phone,
                "skills": json.loads(r.skills_json) if r.skills_json else {},
                "parsed_at": r.parsed_at.isoformat() if r.parsed_at else None
            })
        return jsonify({"total_resumes": len(results), "candidates": results}), 200
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)