from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("form/", views.form_page, name="form_page"),            # <--- ADD THIS LINE
    path("vulnerable/", views.vulnerable_page, name="vulnerable_page"),  # <--- ADD THIS LINE
]
