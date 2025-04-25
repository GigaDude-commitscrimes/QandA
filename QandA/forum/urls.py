from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('vote/<int:answer_id>/<str:vote_type>/', views.vote_answer, name='vote_answer'),
    path('vote/question/<int:question_id>/<str:vote_type>/', views.vote_question, name='vote_question'),
    path('favorite/<int:question_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_questions, name='favorite_questions'),
    path('question/<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('answer/<int:pk>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:pk>/delete/', views.delete_answer, name='delete_answer'),
]
