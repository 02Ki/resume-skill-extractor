from flask import Flask, render_template, request
import spacy
import PyPDF2
import docx

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def extract_skills(text):
    # Predefined skill set
    keywords = [
        "Python", "Java", "C++", "SQL", "JavaScript", "HTML", "CSS", 
        "Machine Learning", "AI", "Data Analysis", "Flask", "React", 
        "Node.js", "Pandas", "NumPy", "TensorFlow", "Keras", "Django"
    ]
    skills_found = [skill for skill in keywords if skill.lower() in text.lower()]
    return skills_found

def suggest_missing_skills(found_skills):
    # Skills important for AI/software jobs
    important_skills = {
        "Programming": ["Python", "Java", "C++"],
        "Web Development": ["HTML", "CSS", "JavaScript", "Flask", "Django", "React", "Node.js"],
        "Data Science": ["SQL", "Pandas", "NumPy", "Data Analysis"],
        "AI/ML": ["Machine Learning", "AI", "TensorFlow", "Keras"]
    }

    suggestions = []
    for category, skills in important_skills.items():
        missing = [s for s in skills if s not in found_skills]
        if missing:
            suggestions.append(f"{category}: {', '.join(missing)}")
    
    return suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_skills = []
    suggestions = []
    if request.method == "POST":
        file = request.files["resume"]
        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            text = file.read().decode("utf-8")

        extracted_skills = extract_skills(text)
        suggestions = suggest_missing_skills(extracted_skills)
    
    return render_template("index.html", skills=extracted_skills, suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True)
