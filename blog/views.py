from django.shortcuts import render, get_object_or_404
from blog.models import Article, Category


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'blog/article_details.html', {'article': article})



def articles_list(request):
    articles = Article.objects.all()
    return render(request, 'blog/articles_list.html', {'articles' : articles})



def category_detail(request, pk=None):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, 'blog/articles_list.html', {'articles' : articles})