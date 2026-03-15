from django.urls import path
from . import views

app_name = 'resume_analyzer'

urlpatterns = [
    path('', views.analyze_resume, name='analyze_resume'),
    path('templates/', views.resume_templates, name='resume_templates'),
    path('create/<int:template_id>/', views.create_resume, name='create_resume'),
    path('preview/<int:resume_id>/', views.preview_resume, name='preview_resume'),
    path('download/<int:resume_id>/', views.download_resume_html, name='download_resume'),
]
