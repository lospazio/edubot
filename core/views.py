from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Discussion, Comment, Note, Exercise, ForumPost, ForumComment
from .forms import MessageForm, DiscussionForm, CommentForm, NoteForm, ExerciseForm, ForumPostForm, ForumCommentForm, AITutorForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.contrib.auth import logout
import openai
from django.conf import settings
from .models import Message
import json
from django.http import JsonResponse
from django.shortcuts import render
import os
import openai
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required


# Dashboard
@login_required
def dashboard(request):
    return render(request, "dashboard.html")

# ---------------------------
# Messaggi privati
# ---------------------------
@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, "messages/inbox.html", {"messages": messages})

@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            return redirect("inbox")
    else:
        form = MessageForm()
    return render(request, "messages/send_message.html", {"form": form})


# ---------------------------
# Discussioni pubbliche
# ---------------------------
# Lista delle discussioni
@login_required
def forum_list(request):
    posts = ForumPost.objects.all().order_by('-created_at')
    return render(request, 'forum/list.html', {'posts': posts})

# Dettaglio di una discussione
@login_required
def forum_detail(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    comments = post.comments.all().order_by('created_at')

    if request.method == "POST":
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('forum_detail', pk=pk)
    else:
        form = ForumCommentForm()

    return render(request, "forum/detail.html", {
    "discussion": post,
    "comments": comments,
    "form": form
    })

# Aggiungi una nuova discussione
@login_required
def forum_add(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum_list')
    else:
        form = ForumPostForm()
    return render(request, 'forum/add.html', {'form': form})


# ---------------------------
# Appunti
# ---------------------------
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/list.html', {'notes': notes})

@staff_member_required  # solo admin possono caricare
def note_upload(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user  # salva chi carica
            note.save()
            return redirect('note_list')  # torna alla lista degli appunti
    else:
        form = NoteForm()
    return render(request, 'notes/upload.html', {'form': form})

# ---------------------------
# Recupero/Potenziamento
# ---------------------------
@login_required
def exercise_list(request):
    exercises = Exercise.objects.all()
    
    subject = request.GET.get('subject')
    type_ = request.GET.get('type')
    level = request.GET.get('level')
    
    if subject:
        exercises = exercises.filter(subject=subject)
    if type_:
        exercises = exercises.filter(tipo=type_)
    if level:
        exercises = exercises.filter(level=level)
    
    return render(request, 'recovery/topics.html', {'exercises': exercises})

@login_required
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    return render(request, 'recovery/exercise_detail.html', {'exercise': exercise})

@login_required
def exercises_home(request):
    return render(request, 'recovery/exercises_home.html')

@login_required
def recupero_list(request):
    # Tutte le materie disponibili
    subjects = Exercise.objects.filter(tipo='recupero').values_list('subject', flat=True).distinct()

    selected_subject = request.GET.get('subject')
    topics = []

    if selected_subject:
        # Recupera gli argomenti della materia selezionata
        topics = Exercise.objects.filter(tipo='recupero', subject=selected_subject)\
                                 .values_list('topic', flat=True).distinct()

    return render(request, 'recovery/recupero_list.html', {
        'subjects': subjects,
        'topics': topics
    })
@login_required
def recupero_detail(request, subject, topic):
    exercises = Exercise.objects.filter(tipo='recupero', subject=subject, topic=topic)
    # Recupera la spiegazione dell'argomento
    explanation = exercises.first().explanation if exercises.exists() else "Spiegazione non disponibile."
    return render(request, 'recovery/recupero_detail.html', {
        'subject': subject,
        'topic': topic,
        'explanation': explanation,
        'exercises': exercises
    })

@login_required
def potenziamento_list(request):
    # Tutte le materie uniche per potenziamento (case-insensitive, strip spazi)
    subjects_qs = Exercise.objects.filter(tipo__iexact='potenziamento')\
                                  .values_list('subject', flat=True)
    subjects_qs = sorted(set(s.strip() for s in subjects_qs))
    subjects = subjects_qs  # qui serve solo la lista semplice per il template

    selected_subject = request.GET.get('subject')
    topics = []

    if selected_subject:
        # Lista argomenti filtrata e unica per la materia selezionata
        topics_qs = Exercise.objects.filter(
            tipo__iexact='potenziamento', 
            subject__iexact=selected_subject
        ).values_list('topic', flat=True)
        topics = sorted(set(t.strip() for t in topics_qs))

    return render(request, 'recovery/potenziamento_list.html', {
        'subjects': subjects,
        'topics': topics
    })

@login_required
def potenziamento_detail(request, subject, topic):
    exercises = Exercise.objects.filter(tipo='potenziamento', subject=subject, topic=topic)
    explanation = exercises.first().explanation if exercises.exists() else "Spiegazione non disponibile."
    return render(request, 'recovery/potenziamento_detail.html', {
        'subject': subject,
        'topic': topic,
        'explanation': explanation,
        'exercises': exercises
    })

# ---------------------------
# Logout e Signup
# ---------------------------

def problem_list(request):
    return redirect('discussion_list')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account creato con successo! Ora puoi fare login.')
            return redirect('login')  # << invece di 'home'
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # oppure home


# ---------------------------
# AI Tutor
# ---------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

# Lista dei messaggi (temporanea, in memoria)
messages = []

def chat_view(request):
    global messages
    if request.method == "POST":
        user_message = request.POST.get("message")
        messages.append({"role": "user", "content": user_message})

        # Chiamata a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        ai_message = response['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": ai_message})

        return JsonResponse({"message": ai_message})

    return render(request, "chat.html", {"messages": messages})