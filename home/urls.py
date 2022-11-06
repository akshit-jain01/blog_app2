from django.contrib import admin
from django.urls import path, include

from .views import BlogView, PublicView

urlpatterns = [
    path('',PublicView.as_view()),
    path('blog/',BlogView.as_view(), name = 'blog')
    
]