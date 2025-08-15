from flask import Flask, render_template, request
import spacy

app = Flask(__name__)

# Ensure the SpaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_skills(text):
    doc = nlp(text)
    skills = set()
    for token in doc:
        if token.pos_ in ["PROPN", "NOUN"] and token.text.lower() not in skills:
            skills.add(token.text)
    return skills


@app.route("/", methods=["GET", "POST"])
def index():
    skills = []
    if request.method == "POST":
        resume_text = request.form["resume"]
        skills = extract_skills(resume_text)
    return render_template("index.html", skills=skills)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

