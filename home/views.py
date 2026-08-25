from django.shortcuts import render
from blog.models import Article, Category
from django.urls import reverse


def home(request):
    articles = Article.objects.all()
    return render(request, 'home/index.html',{'articles' : articles})