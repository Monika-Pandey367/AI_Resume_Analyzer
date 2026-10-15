# AI Resume Analyzer

An intelligent resume analysis web application built using Python and Django. The application helps job seekers compare their resumes with job descriptions, identify relevant skills, and discover areas for improvement.

## Features

- **Resume Upload:** Upload resumes in PDF format.
- **Text Extraction:** Extract text from uploaded resumes.
- **Skill Matching:** Compare resume skills against job description requirements.
- **Matched and Missing Skills:** Identify skills found in the resume and skills that may need improvement.
- **ATS-Style Score:** Calculate a resume-to-job-description match score.
- **Visual Analysis:** Display skill analysis using charts.
- **PDF Report:** Generate a downloadable analysis report.
- **User Authentication:** Register, log in, and log out.
- **Analysis History:** View previous resume analyses.

## Technologies Used

- Python
- Django
- HTML and CSS
- SQLite
- PyPDF2
- Chart.js
- ReportLab

## Project Structure

AI_Resume_Analyzer/
├── analyzer/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── [existing migration files]
│   ├── static/
│   │   └── analyzer/
│   │       └── style.css
│   ├── templates/
│   │   └── analyzer/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── history.html
│   │       └── analysis_detail.html
│   ├── analysis.py
│   ├── recommendation.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── tests.py
├── resume_analyzer/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .gitignore
├── requirements.txt
├── README.md
└── manage.py

## Installation and Setup

### Prerequisites

- Python installed on your computer
- Git installed on your computer

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Resume_Analyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment on Windows

```cmd
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## How It Works

1. Upload a resume in PDF format.
2. Enter the target job description.
3. The application extracts resume text and checks for relevant skills.
4. It identifies matched and missing skills.
5. It calculates a match score and displays the analysis.
6. Download the generated report or review previous analyses.

## Limitations

- The score depends on the application's implemented skill-matching logic.
- The application may not fully understand context or recognize every relevant skill.
- The score is an estimate and does not guarantee ATS compatibility or job selection.

## Future Enhancements

- Improve skill extraction using NLP.
- Add support for additional resume formats.
- Provide more personalized resume improvement recommendations.
- Improve job-description matching accuracy.

## Author

**Monika Pandey**

B.Tech Computer Science and Engineering  
Silver Oak University