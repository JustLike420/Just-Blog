from django.shortcuts import render
from django.views.generic import ListView, DetailView


def index(request):
    return render(request, 'index.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def post(request):
    return render(request, 'post.html', {})
