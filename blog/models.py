from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده مقاله')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    title = models.CharField(max_length=70, verbose_name='عنوان')
    body = models.TextField(verbose_name='متن مقاله')
    image = models.ImageField(upload_to='images/articles', verbose_name='عکس')
    banner = models.ImageField(upload_to='images/banners', blank=True, null=True, verbose_name='بنر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ساخت')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت مقاله')
    status = models.BooleanField(default=True, verbose_name='وضعیت(فعال/غیر فعل)')
    published = models.BooleanField(default=True, verbose_name='منتشر شده')
    slug = models.SlugField(blank=True, unique=True)
    pub_date = models.DateTimeField(default=timezone.now())


    def save( self, force_insert = False, force_update = False, using = None,
            update_fields = None):
        self.slug = slugify(self.title)
        super(Article, self).save()


    def get_absolut_url(self):
        return reverse('blog:article_detail', args=[self.slug])

    def __str__(self):
        return f'{self.title}'

    def show_image(self):
        if self.image:
            return format_html('<img src="{}" width="40px" height="40px" style="object-fit: cover; border-radius: 18%">', self.image.url)
        else:
            return format_html('<h3 style="color: red">تصویر ندارد</h3>')
    show_image.short_description = 'تصویر'

    class Mets:
        ordering = ('-created',)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='نظر والد')

    body = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[:50]

    def show_parent(self):
        if self.parent:
            return format_html('<h3>{}</h3>', self.parent)
        else:
            return mark_safe('<h3 style="color: green">نظر مستقل</h3>')
    show_parent.short_description = 'نظر والد'

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'



class Message(models.Model):
    name = models.CharField(max_length=50, default=None, verbose_name='نام')
    text = models.TextField(verbose_name='متن')
    email = models.EmailField(verbose_name='ایمیل')
    age = models.IntegerField(default=0, verbose_name='سن')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ارسال')


    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='مقاله')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'
        ordering = ('-created_at',)

