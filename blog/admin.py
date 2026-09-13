from django.contrib import admin
from . import models



class FilterByTitle(admin.SimpleListFilter):
    title = 'کلید های پرتکرار'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        return (
        ('django', 'جنگو'),
        ('python', 'پایتون')
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class CommentInline(admin.TabularInline):
    model = models.Comment


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'show_image')
    list_filter = ('status', 'published', FilterByTitle)
    search_fields = ['title', 'body']
    inlines = (CommentInline,)
    # fields = ['']



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age']
    list_filter = ['created_at']


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article']
    list_filter = ['article']



admin.site.register(models.Comment)