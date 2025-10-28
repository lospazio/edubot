# core/sample_data.py
import os
import sys
import django
from datetime import date

# Configura path e Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + os.sep + "..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edubot.settings")
django.setup()

from core.models import Problem, Note, Exercise
from django.contrib.auth.models import User

# ----------------- UTENTI -----------------
if not User.objects.filter(username='alumno').exists():
    User.objects.create_user(username='alumno', password='password123')
    print("Utente 'alumno' creato")

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
    print("Superuser 'admin' creato")

# ----------------- PROBLEMI -----------------
problems_data = [
    {"title":"Equazioni lineari","subject":"math","topic":"Algebra","difficulty":2,"description":"Risolvi x+3=7","solution":"x=4"},
    {"title":"Legge di Newton","subject":"physics","topic":"Dinamica","difficulty":3,"description":"Calcola F=ma","solution":"F= massa * accelerazione"},
    {"title":"Python base","subject":"cs","topic":"Programmazione","difficulty":2,"description":"Scrivi un ciclo for","solution":"for i in range(5): print(i)"},
    {"title":"Sensore ultrasuoni","subject":"robotics","topic":"Sensori","difficulty":2,"description":"Configura un sensore","solution":"Usa modulo HC-SR04"},
    {"title":"Reazioni chimiche","subject":"chem","topic":"Stechiometria","difficulty":3,"description":"Bilancia H2 + O2 -> H2O","solution":"2H2 + O2 -> 2H2O"},
    {"title":"Cellula eucariote","subject":"bio","topic":"Biologia cellulare","difficulty":1,"description":"Descrivi la cellula eucariote","solution":"Ha nucleo e organelli"}
]

for pd in problems_data:
    if not Problem.objects.filter(title=pd["title"]).exists():
        Problem.objects.create(**pd)
print("Problemi creati")

# ----------------- APPUNTI -----------------
notes_data = [
    {"title":"Appunti Matematica","subject":"math","date":date.today(),"file":"notes/sample_math.pdf","highlights":"Equazioni lineari e quadratiche","comments":"Da rivedere"},
    {"title":"Appunti Fisica","subject":"physics","date":date.today(),"file":"notes/sample_physics.pdf","highlights":"Leggi di Newton","comments":"Rivedere dinamica"},
    {"title":"Appunti Informatica","subject":"cs","date":date.today(),"file":"notes/sample_cs.pdf","highlights":"Cicli e funzioni","comments":"Esercizi online"},
    {"title":"Appunti Robotica","subject":"robotics","date":date.today(),"file":"notes/sample_robotics.pdf","highlights":"Sensori e motori","comments":"Mini-progetti"},
    {"title":"Appunti Chimica","subject":"chem","date":date.today(),"file":"notes/sample_chem.pdf","highlights":"Bilanciamento reazioni","comments":"Rivedere formule"},
    {"title":"Appunti Biologia","subject":"bio","date":date.today(),"file":"notes/sample_bio.pdf","highlights":"Cellula eucariote","comments":"Studiare organelli"}
]

for nd in notes_data:
    if not Note.objects.filter(title=nd["title"]).exists():
        Note.objects.create(**nd)
print("Appunti creati")

# ----------------- ESERCIZI -----------------
exercises_data = [
    {"title":"Esercizio Algebra","subject":"math","topic":"Equazioni","level":2,"content":"Risolvi x^2 - 4 = 0","type":"exercise"},
    {"title":"Teoria Dinamica","subject":"physics","topic":"Forze","level":3,"content":"Leggi di Newton","type":"theory"},
    {"title":"Esercizio Python","subject":"cs","topic":"Cicli","level":2,"content":"Scrivi un ciclo for","type":"exercise"},
    {"title":"Teoria Robotica","subject":"robotics","topic":"Sensori","level":2,"content":"Funzionamento sensori","type":"theory"},
    {"title":"Esercizio Chimica","subject":"chem","topic":"Reazioni","level":3,"content":"Bilancia H2 + O2 -> H2O","type":"exercise"},
    {"title":"Teoria Biologia","subject":"bio","topic":"Cellula","level":1,"content":"Struttura cellula eucariote","type":"theory"}
]

for ed in exercises_data:
    if not Exercise.objects.filter(title=ed["title"]).exists():
        Exercise.objects.create(**ed)
print("Esercizi creati")
