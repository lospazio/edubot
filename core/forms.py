# core/forms.py
from django import forms
from .models import Note, Exercise, ForumPost, ForumComment, Message, Discussion, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# -------------------------
# Messaggi privati
# -------------------------
class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ["recipient", "content"]  # sostituiamo 'subject' e 'body' con 'content'

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

# -------------------------
# Discussioni pubbliche
# -------------------------
class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ["title", "description"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

# -------------------------
# Appunti
# -------------------------
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'

# -------------------------
# Materiali di recupero / esercizi
# -------------------------
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'

# -------------------------
# Forum / Chat
# -------------------------
class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['topic', 'content']

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']

# -------------------------
# AI Tutor
# -------------------------
class AITutorForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Scrivi qui la tua domanda...'
    }), label="")
