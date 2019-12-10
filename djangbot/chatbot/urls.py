from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="bot-home"),
    path("about/", views.about, name="bot-about"),
    path("chatt/", views.chatbot, name="chatt"),
    path("bot/", views.bot, name="bot"),
    path("rendering/", views.rendering, name="rendering"),
]

