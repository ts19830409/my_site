from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:pk>/", views.project_detail, name="project_detail"),
    path("certificates/", views.certificates, name="certificates"),
    path("certificates/archive/", views.certificates_archive, name="certificates_archive"),
    path("contacts/", views.contacts, name="contacts"),
    path("awards/", views.awards, name="awards"),
    path('lab/', views.lab, name='lab'),
]
