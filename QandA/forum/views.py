from django.shortcuts import render, get_object_or_404
from .models import Question

def index(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/forums.html', {'questions': questions})

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    return render(request, 'forum/detail.html', {'question': question, 'answers': answers})

def posts(request):
    return render(request, 'forum/posts.html')
