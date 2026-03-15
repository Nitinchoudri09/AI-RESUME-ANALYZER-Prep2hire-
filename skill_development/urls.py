from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('results/', views.results_view, name='quiz_results'),
    path('trending-skills/', views.trending_skills_view, name='trending_skills'),
    path('courses/', views.course_list, name='course_list'),
]
