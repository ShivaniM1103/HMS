from django.urls import path
from . import views

urlpatterns = [
    path('ask/', views.ask_question, name='ask_question'),
    path('chat/', views.chat, name='chat'),
]
