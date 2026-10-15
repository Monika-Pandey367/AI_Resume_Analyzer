from flask import Flask, render_template, request
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

@app.route("/", methods=["GET", "POST"])
def index():
    score = None

    if request.method == "POST":
        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        resume_text = extract_text_from_pdf(resume_file)

        text = [resume_text, job_description]

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text)

        similarity = cosine_similarity(count_matrix)[0][1]
        score = round(similarity * 100, 2)

        return render_template("index.html", score=score)

    return render_template("index.html", score=score)

if __name__ == "__main__":
    app.run(debug=True)