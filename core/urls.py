from django.urls import path
from . import views
from .views import logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Messaggi privati
    path("messages/inbox/", views.inbox, name="inbox"),
    path("messages/send/", views.send_message, name="send_message"),

    # Discussioni (Forum)
    path('discussions/', views.forum_list, name='forum_list'),
    path('discussions/add/', views.forum_add, name='forum_add'),
    path('discussions/<int:pk>/', views.forum_detail, name='forum_detail'),

    # Appunti
    path('notes/', views.note_list, name='note_list'),
    path('notes/upload/', views.note_upload, name='note_upload'),

    # Recupero / Potenziamento (home)
    path('exercises/', views.exercises_home, name='exercises_home'),

    # Recupero
    path('exercises/recupero/', views.recupero_list, name='recupero_list'),
    path('exercises/recupero/<str:subject>/<str:topic>/', views.recupero_detail, name='recupero_detail'),

    # Potenziamento
    path('exercises/potenziamento/', views.potenziamento_list, name='potenziamento_list'),
    path('exercises/potenziamento/<str:subject>/<str:topic>/', views.potenziamento_detail, name='potenziamento_detail'),

    # Autenticazione
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    # AI Tutor
    path("chat/", views.chat_view, name="chat"),
    path("ai-tutor/", views.chat_view, name="ai_tutor"),  # <-- aggiungi questa riga
]
