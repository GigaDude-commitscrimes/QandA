from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('profile/', views.profile, name='profile'),
]
