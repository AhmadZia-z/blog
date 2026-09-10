from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from blog.models import Article, Category, Comment, Message
from django.core.paginator import Paginator
from .forms import ContactUsForm, MessageForm
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView , UpdateView, DeleteView, ArchiveIndexView
from django.urls import reverse, reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import LoginRequiredMixin


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
    return render(request, 'blog/article_detail.html', {'article': article})



def articles_list(request):
    articles = Article.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 2)
    objects_list = paginator.get_page(page_number)
    return render(request, 'blog/article_list.html', {'articles' : objects_list})



def category_detail(request, pk=None):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, 'blog/article_list.html', {'articles' : articles})



def search(request):
    q = request.GET.get('q')
    articles = Article.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 1)
    objects_list = paginator.get_page(page_number)
    return render(request, 'blog/article_list.html', {'articles':objects_list})



def contact_us(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = MessageForm()
    return render(request, 'blog/contact_us.html', {'form':form})




class ArticleList(TemplateView):
    template_name = 'blog/article_list2.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Article.objects.all()
        return context



class HomePageRedirect(RedirectView):
    # url = '/articles/list'
    pattern_name = 'blog:articles_list'
    permanent = False
    query_string = True



class ArticleDetailView(DetailView):          #def article_detail
    model = Article



class ArticleListView(LoginRequiredMixin,ListView):             #def article_list
    model = Article
    context_object_name = 'articles'
    paginate_by = 2
    queryset = Article.objects.filter(published=True)



class ContactUsView(FormView):                 #def contact_us
    template_name = 'blog/contact_us.html'
    form_class = MessageForm
    success_url = reverse_lazy('home:main')

    def form_valid(self, form):
        form_data = form.cleaned_data
        Message.objects.create(**form_data)
        return super().form_valid(form)



class MessageView(CreateView):              #def contact_us
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('home:main')
    template_name = 'blog/contact_us.html'



class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'text', 'age')
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home:main')



class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('home:main')



class ArchiveIndexArticleView(ArchiveIndexView):
    model = Article
    date_field = 'updated'









