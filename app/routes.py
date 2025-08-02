from flask import Flask, Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

# Local modules
from app.resume_store import save_resume_text, get_saved_resume
from app.ml_engine import predict_study_time
from app.youtube_fetcher import fetch_youtube_videos
from app.coursera_fetcher import fetch_coursera_courses
from app.github_fetcher import fetch_github_repos
from app.roadmap_generator import generate_roadmap_for_topic
from app.resume_interview_engine import extract_text_from_resume, generate_interview_questions
from app.utils import log_user_activity

app = Flask(__name__)
main = Blueprint("main", __name__)

# ✅ Health Check
@main.route("/")
def index():
    return jsonify({"message": "✅ AI Study Planner API is running"})

# ✅ Study Time Prediction
@main.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input provided"}), 400

        required_fields = ["free_time_minutes", "days_completed", "engagement_score"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        prediction = predict_study_time(data)

        log_user_activity(
            free_time=data["free_time_minutes"],
            days_completed=data["days_completed"],
            engagement=data["engagement_score"],
            predicted_minutes=prediction
        )

        return jsonify({"predicted_minutes": round(prediction, 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Unified Resource Fetch
@main.route("/api/resources")
def api_resources():
    topic = request.args.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Missing topic parameter"}), 400

    try:
        youtube_videos = []
        coursera_courses = []
        github_repos = []

        try:
            youtube_videos = fetch_youtube_videos(topic)
        except Exception as e:
            print("❌ YouTube error:", e)

        try:
            coursera_courses = fetch_coursera_courses(topic)
        except Exception as e:
            print("❌ Coursera error:", e)

        try:
            github_repos = fetch_github_repos(topic)
        except Exception as e:
            print("❌ GitHub error:", e)

        return jsonify({
            "youtube_videos": youtube_videos,
            "coursera_courses": coursera_courses,
            "github_repos": github_repos
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Roadmap API
@main.route("/api/roadmap", methods=["GET"])
def get_roadmap():
    topic = request.args.get("topic", "")
    if not topic:
        return jsonify({"error": "No topic provided"}), 400
    roadmap = generate_roadmap_for_topic(topic)
    return jsonify({"roadmap": roadmap})

# ✅ Interview Q&A from Resume Upload (with user ID)
@main.route("/api/interview_questions", methods=["POST"])
def interview_questions():
    if "resume" not in request.files or "user_id" not in request.form:
        return jsonify({"error": "Missing resume or user ID"}), 400

    user_id = request.form["user_id"]
    file = request.files["resume"]
    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    try:
        resume_text = extract_text_from_resume(filepath)
        print("📄 Resume Content:\n", resume_text[:500])  # Debug print for verification

        save_resume_text(user_id, resume_text)  # ✅ Store for future use
        qa = generate_interview_questions(resume_text)
        return jsonify({"questions": qa})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Generate Q&A from raw resume text (Blueprint route)
@main.route("/api/generate-questions", methods=["POST"])
def generate_questions_from_text():
    data = request.get_json()
    if not data or "resume_text" not in data:
        return jsonify({"error": "Missing resume_text in request"}), 400

    try:
        qa_pairs = generate_interview_questions(data["resume_text"])
        return jsonify({"qaPairs": qa_pairs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Generate Q&A using "resumeText" (Blueprint route)
@main.route("/api/interview", methods=["POST"])
def generate_questions_blueprint():
    try:
        data = request.get_json()
        if not data or "resumeText" not in data:
            return jsonify({"error": "Missing resumeText in request"}), 400

        resume_text = data["resumeText"]
        qa_pairs = generate_interview_questions(resume_text)
        return jsonify({"qaPairs": qa_pairs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Retrieve Saved Resume
@main.route("/api/saved_resume", methods=["GET"])
def get_saved():
    user_id = request.args.get("user_id", "")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    resume_text = get_saved_resume(user_id)
    if not resume_text:
        return jsonify({"error": "No saved resume found"}), 404

    return jsonify({"resume": resume_text})


# ✅ NEW: Raw Flask route (not inside Blueprint)
@app.route("/generate-questions", methods=["POST"])
def generate_questions_simple():
    try:
        resume_text = request.json.get("resumeText")
        qa_pairs = generate_interview_questions(resume_text)
        return jsonify(qa_pairs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Register Blueprint
app.register_blueprint(main)
