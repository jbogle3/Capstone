"""
URL configuration for mysite project.
... (docstring) ...
"""
from django.contrib import admin
from django.urls import include, path
from polls import views as polls_views  # <--- ADD THIS IMPORT

urlpatterns = [
    path("", polls_views.home, name="home"),  # <--- ADD THIS LINE (Home Page)
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
