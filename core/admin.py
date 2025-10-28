# edubot/admin.py
from django.contrib import admin
from .models import Exercise , Note

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'topic', 'tipo', 'explanation')
    list_filter = ('subject', 'tipo', 'topic')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at')  # colonne visibili
    list_filter = ('uploaded_by', 'uploaded_at')           # filtri laterali
    search_fields = ('title', 'uploaded_by__username')    # barra di ricerca
