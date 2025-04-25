"""
URL configuration for QandA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from django.contrib.auth import views as auth_views
from forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='forum/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('vote/<int:answer_id>/<str:vote_type>/', views.vote_answer, name='vote_answer'),
    path('favorites/', views.favorite_questions, name='favorite_questions'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='forum/login.html', next_page='profile'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]