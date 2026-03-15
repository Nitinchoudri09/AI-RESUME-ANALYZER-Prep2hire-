from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'), 
    path('carrer_recommendation/', views.career_quiz, name='carrer_recommendation'),
    path('connect/', views.post_list, name='post_list'),
    path('connect/new/', views.create_post, name='create_post'),
    path('connect/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('connect/like/<int:post_id>/', views.like_post, name='like_post'),
    path('dashboard/', views.dashboard, name='dashboard')
]
