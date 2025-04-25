from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Count, Sum
from .models import Question, Answer, Vote, Tag

# Главная страница
def index(request):
    questions = Question.objects.all().annotate(  # Добавляем сумму голосов
        vote_sum=Sum('votes__value')
    ).order_by('-created_at')
    return render(request, 'forum/forums.html', {'questions': questions})

# Детальная страница вопроса с ответами
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question.vote_sum = question.votes.aggregate(total=Sum('value'))['total'] or 0
    answers = question.answers.all().annotate(vote_sum=Sum('votes__value')).order_by('-vote_sum', '-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Answer.objects.create(question=question, content=content, author=request.user)
            return redirect('question_detail', pk=pk)

    return render(request, 'forum/detail.html', {'question': question, 'answers': answers})

# Задать вопрос
@login_required
def ask_question(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_ids = request.POST.getlist('tags')
        question = Question.objects.create(title=title, content=content, author=request.user)
        question.tags.set(tag_ids)
        return redirect('index')
    return render(request, 'forum/ask_question.html', {'tags': tags})

# Профиль пользователя
@login_required
def profile(request):
    user_questions = Question.objects.filter(author=request.user)
    favorite_questions = request.user.favorite_questions.all()
    return render(request, 'forum/profile.html', {
        'user_questions': user_questions,
        'favorite_questions': favorite_questions
    })

# Редактирование профиля
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'forum/edit_profile.html', {'form': form})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'forum/register.html', {'form': form})

# Голосование за ответ
@login_required
def vote_answer(request, answer_id, vote_type):
    answer = get_object_or_404(Answer, id=answer_id)
    vote, created = Vote.objects.get_or_create(answer=answer, user=request.user, defaults={'value': 1 if vote_type == 'up' else -1})

    if not created:
        vote.value = 1 if vote_type == 'up' else -1
        vote.save()

    return redirect('question_detail', pk=answer.question.id)

def posts(request):
    return render(request, 'forum/posts.html')

# Голосования за вопросы 
@login_required
def vote_question(request, question_id, vote_type):
    question = get_object_or_404(Question, id=question_id)
    question.vote_sum = question.votes.aggregate(total=Sum('value'))['total'] or 0
    vote, created = Vote.objects.get_or_create(question=question, user=request.user, defaults={'value': 1 if vote_type == 'up' else -1})

    vote.value = 1 if vote_type == 'up' else -1
    vote.save()

    return redirect('question_detail', pk=question.id)

# Функция для добавления/удаления из избранного.
@login_required
def toggle_favorite(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user in question.favorites.all():
        question.favorites.remove(request.user)
    else:
        question.favorites.add(request.user)
    return redirect('question_detail', pk=question.id)

@login_required
def favorite_questions(request):
    favorites = request.user.favorite_questions.all()
    return render(request, 'forum/favorites.html', {'favorites': favorites})

# Редактирование вопроса
@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk, author=request.user)
    if request.method == 'POST':
        question.title = request.POST.get('title')
        question.content = request.POST.get('content')
        question.save()
        return redirect('question_detail', pk=question.id)
    return render(request, 'forum/edit_question.html', {'question': question})

# Удаление вопроса
@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk, author=request.user)
    if request.method == 'POST':
        question.delete()
        return redirect('index')
    return render(request, 'forum/delete_question.html', {'question': question})

# Редактирование ответа
@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk, author=request.user)
    if request.method == 'POST':
        answer.content = request.POST.get('content')
        answer.save()
        return redirect('question_detail', pk=answer.question.id)
    return render(request, 'forum/edit_answer.html', {'answer': answer})

# Удаление ответа
@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk, author=request.user)
    if request.method == 'POST':
        question_id = answer.question.id
        answer.delete()
        return redirect('question_detail', pk=question_id)
    return render(request, 'forum/delete_answer.html', {'answer': answer})