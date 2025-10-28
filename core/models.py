# core/models.py
from django.db import models
from django.contrib.auth.models import User

# -------------------------
# Messaggi privati
# -------------------------
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.subject}"

class Discussion(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -------------------------
# Discussioni pubbliche
# -------------------------
class Discussion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.discussion.title}"

# -------------------------
# Appunti
# -------------------------
class Note(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # <-- assicurati che ci sia
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
# -------------------------
# Materiali di recupero / esercizi
# -------------------------
class Exercise(models.Model):
    TIPO_CHOICES = [
        ('recupero', 'Recupero'),
        ('potenziamento', 'Potenziamento'),
    ]

    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='recupero')
    explanation = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):
        # Se non c’è spiegazione, impostane una di default in base al tipo
        if not self.explanation:
            if self.tipo == 'recupero':
                self.explanation = 'Ripassa bene questo argomento prima di procedere!'
            elif self.tipo == 'potenziamento':
                self.explanation = 'Ottimo lavoro! Prova a spingerti oltre con esercizi avanzati.'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.tipo})"

# -------------------------
# Forum / Chat
# -------------------------
class ForumPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} ({self.author})"


class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.topic}"

# -------------------------
# AI Tutor
# -------------------------
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.recipient}: {self.content[:20]}'

