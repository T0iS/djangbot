from django.urls import path
from . import views

urlpatterns = [
    path("about/", views.about, name="bot-about"),
    path("bot/", views.bot, name="bot"),
    path("", views.rendering, name="rendering"),
]

