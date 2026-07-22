import os
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "poonam_portfolio")

# ---------- Email (Gmail SMTP) ----------
# GMAIL_USER / GMAIL_APP_PASSWORD send the mail.
# NOTIFY_EMAIL is where the notification lands (defaults to your own inbox).
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", GMAIL_USER)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client[MONGO_DB]

# Collections
experience_col = db["experience"]
projects_col = db["projects"]
skills_col = db["skills"]
education_col = db["education"]
stats_col = db["stats"]
messages_col = db["messages"]

# ---------- Fallback data ----------
# Used only if MongoDB is unreachable or a collection is empty,
# so the site never breaks in front of a recruiter.
FALLBACK = {
    "experience": [
        {
            "order": 1,
            "status": "current",
            "time": "Nov 2025 — May 2026",
            "title": "Web Developer Assistant Intern",
            "org": "Indian Chamber of Food & Agriculture (ICFA)",
            "bullets": [
                "Redesigned the IACG portal with a modern UI/UX and responsive layout, improving accessibility and stakeholder engagement.",
                "Built a PHP/MySQL/JavaScript Employee Management System with secure admin controls, automated lifecycle workflows, and full API handling.",
                "Developed the CACL Kisan Connect platform to centralise information access for agricultural stakeholders.",
            ],
        },
        {
            "order": 2,
            "status": "",
            "time": "Jul 2025 — Aug 2025",
            "title": "IT Unit Intern",
            "org": "Power Finance Corporation (PFC)",
            "bullets": [
                "Audited IT workflows across HR and IT departments and delivered a technical efficiency report with prioritised recommendations.",
                "Assessed infrastructure processes and proposed targeted improvements to boost operational efficiency.",
            ],
        },
        {
            "order": 3,
            "status": "",
            "time": "Jul 2024 — Aug 2024",
            "title": "Web Development Intern",
            "org": "Centre for Railway Information Systems (CRIS)",
            "bullets": [
                "Worked alongside software engineers to enhance frontend functionality and accessibility of Indian Railways web applications.",
                "Contributed to interface optimisation initiatives that improved usability across high-traffic government portals.",
            ],
        },
        {
            "order": 4,
            "status": "",
            "time": "Jan 2023 — Apr 2023",
            "title": "Java Developer Intern",
            "org": "BiSAG-N, Ministry of Electronics & IT (MeitY)",
            "bullets": [
                "Developed backend modules in Java, Spring Boot, Hibernate, and PostgreSQL for scalable government-facing applications.",
                "Participated across the full SDLC — from development and testing through to deployment.",
            ],
        },
    ],
    "projects": [
        {
            "index": "01",
            "title": "Ransomware Detection Tool",
            "description": "A monitoring system that flags suspicious file activity and system anomalies through real-time log analysis — catching rapid file modifications and known ransomware patterns on an interactive dashboard.",
            "tags": ["Python", "Flask", "MySQL", "JavaScript"],
        },
        {
            "index": "02",
            "title": "Travel With Us",
            "description": "A full-stack travel management app with end-to-end booking workflows, a secure admin panel, and complete CRUD functionality — with all APIs tested and documented through Postman.",
            "tags": ["PHP", "MySQL", "JavaScript", "Postman"],
        },
        {
            "index": "03",
            "title": "iBanking System",
            "description": "A simulated banking platform covering fund transfers, account management, and secure authentication — built on a normalised PostgreSQL schema for transaction consistency and audit readiness.",
            "tags": ["Java", "Spring MVC", "Hibernate", "PostgreSQL"],
        },
    ],
    "skills": [
        {"group": "Languages", "items": ["Python", "Java", "C", "PHP"]},
        {"group": "Web", "items": ["HTML5", "CSS3", "JavaScript"]},
        {"group": "Frameworks", "items": ["Flask", "FastAPI", "Spring Boot", "React.js", "Node.js", "Express.js", "REST APIs", "Postman"]},
        {"group": "ML / Data Science", "items": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn", "PyTorch", "Statistics & Probability"]},
        {"group": "Tools", "items": ["Git", "GitHub", "Docker"]},
        {"group": "Databases & Fundamentals", "items": ["PostgreSQL", "MySQL", "MongoDB", "OOP", "DBMS"]},
    ],
    "education": [
        {"year": "2023 — 2026", "degree": "B.Tech, Computer Science Engineering", "school": "Guru Tegh Bahadur 4th Centenary Engineering College, Delhi", "score": "89%"},
        {"year": "2020 — 2023", "degree": "Diploma, ITES&M", "school": "Ambedkar Institute of Technology, Delhi", "score": "81%"},
        {"year": "2020", "degree": "Class X, CBSE", "school": "Navyug School, Peshwa Road, New Delhi", "score": "65%"},
    ],
    "stats": [
        {"num": "4", "label": "INTERNSHIPS"},
        {"num": "3", "label": "FULL-STACK PROJECTS"},
        {"num": "2026", "label": "GRADUATION YEAR"},
    ],
}

def send_email_notification(name, email, message):
    """Send the contact-form message to Gmail. Never raises — a failed email
    should not block saving the message to MongoDB."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        app.logger.warning("Email not configured: set GMAIL_USER and GMAIL_APP_PASSWORD in .env")
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio contact: {name}"
    msg["From"] = GMAIL_USER
    msg["To"] = NOTIFY_EMAIL
    msg["Reply-To"] = email  # so hitting "Reply" in Gmail replies straight to the sender
    msg.set_content(
        f"New message from your Portfolio site\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}\n"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as exc:
        app.logger.error(f"Email send failed: {exc}")
        return False

def get_collection_or_fallback(collection, key):
    """Read from MongoDB; fall back to static data if the DB is empty or unreachable."""
    try:
        docs = list(collection.find({}, {"_id": 0}).sort("order", 1) if key == "experience" else collection.find({}, {"_id": 0}))
        if docs:
            return docs
    except PyMongoError:
        pass
    return FALLBACK[key]

@app.route("/")
def home():
    context = {
        "experience": get_collection_or_fallback(experience_col, "experience"),
        "projects": get_collection_or_fallback(projects_col, "projects"),
        "skills": get_collection_or_fallback(skills_col, "skills"),
        "education": get_collection_or_fallback(education_col, "education"),
        "stats": get_collection_or_fallback(stats_col, "stats"),
    }
    return render_template("index.html", **context)

@app.route("/api/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or request.form
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return jsonify({"ok": False, "error": "Please fill in name, email, and message."}), 400

    doc = {
        "name": name,
        "email": email,
        "message": message,
        "created_at": datetime.now(timezone.utc),
    }

    try:
        messages_col.insert_one(doc)
    except PyMongoError:
        return jsonify({"ok": False, "error": "Could not save your message right now. Please try emailing directly."}), 500

    # Best-effort email notification — message is already safely stored in
    # MongoDB above, so a failed email here doesn't lose the message.
    email_sent = send_email_notification(name, email, message)

    return jsonify({
        "ok": True,
        "message": "Thanks! Your message has been received." if email_sent
                   else "Thanks! Your message has been saved (email notification is not configured yet).",
    })

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug, host="0.0.0.0", port=5000)