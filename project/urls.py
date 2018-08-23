# encoding: utf-8
from django.urls import path
from virkamiesbot.views import Index

urlpatterns = [
    path('', Index.as_view()),
]
