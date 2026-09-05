import json
import os
import traceback
from flask import (
    Flask, jsonify, redirect, render_template, request,
    send_from_directory, url_for
)
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user
)
from werkzeug.utils import secure_filename

import config
from database import (
    ResumeRecord, SessionLocal, User, init_db, save_parsed_resume
)
from nlp.parser import parse_resume

app = Flask(__name__)
app.secret_key = "reddy_ai_secret_key_8888"
app.config["UPLOAD_FOLDER"] = os.path.abspath(config.UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

# Ensure upload directory exists immediately on server start
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

login_manager = LoginManager()
login_manager.login_view = "index"
login_manager.init_app(app)

init_db()

@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    try:
        return session.query(User).get(int(user_id))
    finally:
        session.close()

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS

# ================= AUTHENTICATION REST API =================

@app.route("/api/register", methods=["POST"])
def api_register():
    try:
        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not username or not email or not password:
            return jsonify({"error": "All fields are required."}), 400

        session = SessionLocal()
        try:
            existing = session.query(User).filter((User.username == username) | (User.email == email)).first()
            if existing:
                return jsonify({"error": "Username or Email already registered."}), 409

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            login_user(new_user)
            return jsonify({"message": "Registration successful", "username": new_user.username}), 201
        finally:
            session.close()
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route("/api/login", methods=["POST"])
def api_login():
    try:
        data = request.get_json(force=True, silent=True) or {}
        identifier = data.get("identifier", "").strip()
        password = data.get("password", "")

        if not identifier or not password:
            return jsonify({"error": "Username/Email and password are required."}), 400

        session = SessionLocal()
        try:
            user = session.query(User).filter(
                (User.username == identifier) | (User.email == identifier.lower())
            ).first()
            
            if user and user.check_password(password):
                login_user(user)
                return jsonify({"message": "Login successful", "username": user.username}), 200
            return jsonify({"error": "Invalid credentials. Please try again."}), 401
        finally:
            session.close()
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# ================= MAIN & RESUME ENDPOINTS =================

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/parse", methods=["POST"])
@login_required
def upload_and_parse():
    if "resume" not in request.files:
        return jsonify({"error": "No resume file provided."}), 400

    file = request.files["resume"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        safe_base = secure_filename(file.filename)
        user_specific_filename = f"u{current_user.id}_{safe_base}"
        save_path = os.path.abspath(os.path.join(app.config["UPLOAD_FOLDER"], user_specific_filename))
        
        file.save(save_path)

        try:
            parsed_data = parse_resume(save_path)
            record_id = save_parsed_resume(current_user.id, user_specific_filename, parsed_data)
            return jsonify({
                "message": "Resume parsed and saved to your private vault.",
                "candidate_id": record_id,
                "data": parsed_data
            }), 201
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"Failed to process resume: {str(e)}"}), 500

    return jsonify({"error": "Only .pdf and .docx file formats are supported."}), 400

@app.route("/api/resumes", methods=["GET"])
@login_required
def get_user_resumes():
    session = SessionLocal()
    try:
        records = session.query(ResumeRecord).filter(ResumeRecord.user_id == current_user.id).order_by(ResumeRecord.id.desc()).all()
        results = []
        for r in records:
            results.append({
                "id": r.id,
                "filename": r.filename,
                "candidate_name": r.candidate_name,
                "email": r.email,
                "phone": r.phone,
                "skills": json.loads(r.skills_json) if r.skills_json else {},
                "education": r.education_text,
                "experience": r.experience_text,
                "projects": r.projects_text,
                "parsed_at": r.parsed_at.isoformat() if r.parsed_at else None
            })
        return jsonify({"total_resumes": len(results), "candidates": results}), 200
    finally:
        session.close()

@app.route("/api/download/<filename>", methods=["GET"])
@login_required
def download_file(filename: str):
    safe_name = secure_filename(filename)
    session = SessionLocal()
    try:
        record = session.query(ResumeRecord).filter(
            ResumeRecord.filename == safe_name,
            ResumeRecord.user_id == current_user.id
        ).first()

        if not record:
            return jsonify({"error": "Unauthorized or file not found."}), 403

        return send_from_directory(app.config["UPLOAD_FOLDER"], safe_name, as_attachment=True)
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)