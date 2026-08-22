from django.shortcuts import render
from blog.models import Article, Caregory
from django.urls import reverse


def home(request):
    articles = Article.objects.all()
    recent_articles = Article.objects.all().order_by('-created')[:3]
    category = Caregory.objects.all()
    return render(request, 'home/index.html',{'articles' : articles, 'recent_articles' : recent_articles, 'category' : category})