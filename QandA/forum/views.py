from django.shortcuts import render, get_object_or_404, redirect
from .models import Question
from django.contrib.auth.decorators import login_required

def index(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/forums.html', {'questions': questions})

def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    return render(request, 'forum/detail.html', {'question': question, 'answers': answers})

def posts(request):
    return render(request, 'forum/posts.html')

@login_required
def ask_question(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Question.objects.create(title=title, content=content, author=request.user)
        return redirect('index')
    return render(request, 'forum/ask_question.html')

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user_questions = Question.objects.filter(author=request.user)
    return render(request, 'forum/profile.html', {'user_questions': user_questions})
