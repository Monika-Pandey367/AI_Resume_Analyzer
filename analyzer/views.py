from .models import ResumeAnalysis
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import PyPDF2
from django.contrib import messages
import string
import re
from .recommendation import generate_recommendation
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pathlib import Path
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Check whether the PDF contains any pages
        if len(reader.pages) == 0:
            return None

        # Extract text from every page
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        # Check whether any text was extracted
        if not text.strip():
            return None

        return text

    except (
        PyPDF2.errors.PdfReadError,
        ValueError,
        OSError,
    ):
        return None

def extract_skills(text):
    if not text:
        return []

    # Load the technology catalogue
    catalogue_path = Path(__file__).resolve().parent / "technology_skills.json"

    with open(catalogue_path, "r", encoding="utf-8") as file:
        catalogue = json.load(file)

    skills = catalogue["skills"]
    aliases = catalogue.get("aliases", {})

    detected_skills = []
    cleaned_text = text.lower()

    for skill in skills:
        # Check the official skill name and its aliases
        names_to_check = [skill] + aliases.get(skill, [])

        for name in names_to_check:
            pattern = r"(?<!\w)" + re.escape(name.lower()) + r"(?!\w)"

            if re.search(pattern, cleaned_text):
                detected_skills.append(skill)
                break

    return detected_skills

def get_ats_status(ats_score):
    if ats_score>=80:
        ats_status="Excellent Match"
    elif ats_score>=60:
        ats_status="Good match"
    elif ats_score>=40:        
        ats_status="Average Match"
    else :                                  
        ats_status="Poor match"
    return ats_status

from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generate_pdf(request):
    print("generate_pdf called")

    if "ats_score" not in request.session:
        return redirect("home")
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Resume_Report.pdf"'

    pdf = canvas.Canvas(response)

    ats_score = request.session.get("ats_score", "Not Available")
    ats_status = request.session.get("ats_status", "Not Available")
    matched_skills = request.session.get("matched_skills", [])
    missing_skills = request.session.get("missing_skills", [])
    recommendations = request.session.get("recommendations", [])

    print("ATS:", ats_score)
    print("Status:", ats_status)
    print("Matched:", matched_skills)
    print("Missing:", missing_skills)
    print("Recommendations:", recommendations)

    y = 800

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(150, y, "AI Resume Analyzer Report")

    y -= 40
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"ATS Score : {ats_score}")

    y -= 20
    pdf.drawString(50, y, f"ATS Status : {ats_status}")

    y -= 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Matched Skills")

    pdf.setFont("Helvetica", 12)

    for skill in matched_skills:
        y -= 20
        pdf.drawString(70, y, f"- {skill}")

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Missing Skills")

    pdf.setFont("Helvetica", 12)

    for skill in missing_skills:
        y -= 20
        pdf.drawString(70, y, f"- {skill}")

    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Recommendations")

    pdf.setFont("Helvetica", 12)

    for rec in recommendations:
        y -= 20
        pdf.drawString(70, y, f"- {rec}")

    pdf.save()

    return response

def home(request):
    recommendations = []
    message = ""
    guest_message = ""
    extracted_text = ""
    detected_skills = []
    jd_skills = []
    matched_skills = []
    missing_skills = []
    ats_score = 0
    ats_status = ""
    analysis_done = False

    if request.method == "POST":
        analysis_done = True

        resume = request.FILES.get("resume")

        if not resume:
            message = "Please upload a resume PDF."
            return render(request, "analyzer/index.html", {
                "message": message,
                "analysis_done": False,
            })

        if not resume.name.lower().endswith(".pdf"):
            message = "Invalid file type. Please upload a PDF file only."
            return render(request, "analyzer/index.html", {
                "message": message,
                "analysis_done": False,
            })

        job_description = request.POST.get("job_description", "")
# Extract resume text
        extracted_text = extract_text_from_pdf(resume)

        # Handle damaged or unreadable PDFs
        if extracted_text is None:
            message = (
                "Unable to read this PDF. "
                "Please upload a valid, text-based PDF resume."
            )

            return render(request, "analyzer/index.html", {
                "message": message,
                "analysis_done": False,
            })

        # Extract skills
        detected_skills = extract_skills(extracted_text)
        jd_skills = extract_skills(job_description)
        resume_skill_set = set(detected_skills)
        jd_skill_set = set(jd_skills)


        matched_skills = sorted(resume_skill_set & jd_skill_set)
        missing_skills = sorted(jd_skill_set - resume_skill_set)

        recommendations = generate_recommendation(missing_skills)

        if len(jd_skill_set) > 0:
            ats_score = round(
                (len(matched_skills) / len(jd_skill_set)) * 100,
                2
            )
        else:
            ats_score = 0

        ats_status = get_ats_status(ats_score)

        if request.user.is_authenticated:
            ResumeAnalysis.objects.create(
                user=request.user,
                resume_name=resume.name,
                ats_score=ats_score,
                ats_status=ats_status,
                matched_skills=", ".join(matched_skills),
                missing_skills=", ".join(missing_skills),
                recommendations=", ".join(recommendations)
            )
        else:
            request.session["pending_analysis"] = {
                "resume_name": resume.name,
                "ats_score": ats_score,
                "ats_status": ats_status,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "recommendations": recommendations,
            }

            guest_message = (
                "Your analysis is ready! "
                "Register or log in to save your results "
                "and access your analysis history later."
            )

        # Keep these for the PDF download feature.
        request.session["ats_score"] = ats_score
        request.session["ats_status"] = ats_status
        request.session["matched_skills"] = matched_skills
        request.session["missing_skills"] = missing_skills
        request.session["recommendations"] = recommendations

        # Mark that an analysis was just performed.
        request.session["show_analysis"] = True

    elif request.method == "GET":
        # Hide the result on a normal page refresh.
        if request.session.get("show_analysis"):
            request.session["show_analysis"] = False

    # Show results only immediately after analysis.
    analysis_done = (
        request.method == "POST"
        and analysis_done
    )

    return render(request, "analyzer/index.html", {
        "extracted_text": extracted_text,
        "detected_skills": detected_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "recommendations": recommendations,
        "ats_status": ats_status,
        "message": message,
        "guest_message": guest_message,
        "analysis_done": analysis_done,
    })

@login_required
@login_required
def history(request):
    analyses = ResumeAnalysis.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "analyzer/history.html", {
        "analyses": analyses
    })
@login_required
def delete_analysis(request, id):
    analysis = get_object_or_404(
        ResumeAnalysis,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        analysis.delete()

    return redirect("history")
@login_required
def analysis_detail(request, id):
    analysis = get_object_or_404(
        ResumeAnalysis,
        id=id,
        user=request.user
    )

    return render(request, "analyzer/analysis_detail.html", {
        "analysis": analysis
    })

@login_required
def download_history_pdf(request, id):

    analysis = get_object_or_404(
        ResumeAnalysis,
        id=id,
        user=request.user
    )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="Resume_Report.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        150,
        800,
        "AI Resume Analyzer Report"
    )

    y = 760

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        y,
        f"Resume: {analysis.resume_name}"
    )

    y -= 30

    pdf.drawString(
        50,
        y,
        f"ATS Score: {analysis.ats_score}%"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"ATS Status: {analysis.ats_status}"
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Matched Skills"
    )

    pdf.setFont("Helvetica", 12)

    for skill in analysis.matched_skills.split(", "):

        y -= 20

        pdf.drawString(
            70,
            y,
            f"- {skill}"
        )

    y -= 30

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Missing Skills"
    )

    pdf.setFont("Helvetica", 12)

    if analysis.missing_skills:

        for skill in analysis.missing_skills.split(", "):

            y -= 20

            pdf.drawString(
                70,
                y,
                f"- {skill}"
            )

    else:

        y -= 20

        pdf.drawString(
            70,
            y,
            "None"
        )

    y -= 30

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Recommendations"
    )

    pdf.setFont("Helvetica", 12)
    if analysis.recommendations:
        for recommendation in analysis.recommendations.split(", "):
            y -= 20
            pdf.drawString(
                70,
                y,
                f"- {recommendation}"
            )
    else:
        y -= 20
        pdf.drawString(
            70,
            y,
            "None"
        )
    pdf.save()
    return response



def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"]
        if len(password) < 8:
                    error = "Password must contain at least 8 characters."
        elif not re.search(r"[A-Za-z]", password):
                    error = "Password must contain at least one letter."
        elif not re.search(r"\d", password):
                    error = "Password must contain at least one number."
        else:
                    error = ""

        if error:
                    return render(request, "analyzer/register.html", {
                        "error": error,
                    })
            # Check whether the username already exists
        if User.objects.filter(username=username).exists():
                return render(request, "analyzer/register.html", {
                    "error": " User already exists. Please choose another username."
                })

        user = User.objects.create_user(
                username=username,
                password=password
            )

            # Automatically log in the new user
        login(request, user)

            # Save the pending guest analysis, if available
        pending = request.session.get("pending_analysis")

        if pending:
                ResumeAnalysis.objects.create(
                    user=user,
                    resume_name=pending["resume_name"],
                    ats_score=pending["ats_score"],
                    ats_status=pending["ats_status"],
                    matched_skills=", ".join(
                        pending["matched_skills"]
                    ),
                    missing_skills=", ".join(
                        pending["missing_skills"]
                    ),
                    recommendations=", ".join(
                        pending["recommendations"]
                    )
                )

                del request.session["pending_analysis"]

        return redirect("home")

    return render(request, "analyzer/register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            # Retrieve a guest's pending analysis
            pending = request.session.get("pending_analysis")

            if pending:
                ResumeAnalysis.objects.create(
                    user=user,
                    resume_name=pending["resume_name"],
                    ats_score=pending["ats_score"],
                    ats_status=pending["ats_status"],
                    matched_skills=", ".join(
                        pending["matched_skills"]
                    ),
                    missing_skills=", ".join(
                        pending["missing_skills"]
                    ),
                    recommendations=", ".join(
                        pending["recommendations"]
                    )
                )

                # Clear it after saving
                del request.session["pending_analysis"]

            return redirect("home")

        return render(request, "analyzer/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "analyzer/login.html")

def user_logout(request):
    logout(request)
    return redirect("login")