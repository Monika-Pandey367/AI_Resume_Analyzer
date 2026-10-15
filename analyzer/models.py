from django.db import models
from django.contrib.auth.models import User


class ResumeAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_name = models.CharField(max_length=255)
    ats_score = models.FloatField()
    ats_status = models.CharField(max_length=50)
    matched_skills = models.TextField()
    missing_skills = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)