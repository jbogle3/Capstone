from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.form_page, name="form_page"),
    path("vulnerable/", views.vulnerable_page, name="vulnerable_page"),
    path("upload/", views.upload_analysis, name="upload_analysis"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logs/", views.security_logs, name="security_logs"),
]
