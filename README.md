```markdown
# Personal Portfolio Website

A dynamic full-stack personal portfolio website built with Python (Flask), HTML5, CSS3, and JavaScript, configured for deployment on Render using Gunicorn.

🌐 **Live Demo:** [poonam-portfolio-f2bw.onrender.com](https://poonam-portfolio-f2bw.onrender.com/)

---

## 🚀 Features

- **Responsive Design:** Optimized for mobile, tablet, and desktop viewing.
- **Dynamic Content:** Rendered via Flask templates.
- **Database Integration:** Includes database seeding capabilities (`seed_db.py`).
- **Contact / Email Integration:** Automated email messaging integration tested via `test_email.py`.
- **Production Ready:** Pre-configured with Gunicorn for deployment.

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask), Gunicorn
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Render

---

## 📂 Project Structure

```text
poonam-portfolio/
├── static/              # CSS stylesheets, JavaScript files, and images
├── templates/           # HTML templates (Jinja2)
├── .gitignore           # Git ignore file
├── app.py               # Main Flask application entry point
├── requirements.txt     # Python dependencies
├── seed_db.py           # Database population/seeding script
├── test_email.py        # Email integration testing script
└── README.md            # Project documentation

```

---

## ⚙️ Getting Started

### Prerequisites

* Python 3.8+ installed on your local machine
* `git` installed

### Installation & Local Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/poonam-webdev/poonam-portfolio.git](https://github.com/poonam-webdev/poonam-portfolio.git)
cd poonam-portfolio

```


2. **Create and activate a virtual environment:**
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

```


3. **Install required dependencies:**
```bash
pip install -r requirements.txt

```


4. **Seed the database (if required):**
```bash
python seed_db.py

```


5. **Run the application:**
```bash
python app.py

```


6. Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 🌐 Deployment

This application is ready to deploy on **Render** (or platforms like Railway/Heroku):

* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`

---

## 👤 Author

**Poonam Kumari**

* GitHub: [@poonam-webdev](https://github.com/poonam-webdev)

```

```
