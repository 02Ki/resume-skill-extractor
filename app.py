from flask import Flask, render_template, request
import spacy
import os
import PyPDF2
import docx

app = Flask(__name__)

# Predefined list of skills
SKILL_SET = [
    "Python", "Java", "C++", "C", "JavaScript", "TypeScript",
    "HTML", "CSS", "React", "Node.js", "Flask", "Django",
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Pandas", "NumPy", "Matplotlib", "Data Analysis",
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
    "Git", "GitHub", "Power BI", "Excel", "Tableau"
]

# Load SpaCy model for tokenization
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_text_from_file(file):
    """Extract text from PDF, DOCX, or TXT file."""
    text = ""
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")
    return text

def extract_skills(text):
    """Extract skills from resume text based on predefined list."""
    found_skills = set()
    text_lower = text.lower()
    for skill in SKILL_SET:
        if skill.lower() in text_lower:
            found_skills.add(skill)
    return sorted(found_skills)

@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    if request.method == "POST":
        if "resume" not in request.files:
            return "No file uploaded", 400
        
        file = request.files["resume"]
        if file.filename == "":
            return "No file selected", 400

        resume_text = extract_text_from_file(file)
        if not resume_text.strip():
            return "Could not read the file or file is empty", 400

        skills = extract_skills(resume_text)

    return render_template("index.html", skills=skills)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
