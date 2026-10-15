from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("download/", views.generate_pdf, name="download_pdf"),
    path("history/", views.history, name="history"),
    path("history/<int:id>/", views.analysis_detail, name="analysis_detail"),
path(
    "history/<int:id>/pdf/",
    views.download_history_pdf,
    name="download_history_pdf"
),
path("register/", views.register, name="register"),
path("login/", views.user_login, name="login"),
path("logout/", views.user_logout, name="logout"),
path(
    "history/<int:id>/delete/",
    views.delete_analysis,
    name="delete_analysis"
),
]