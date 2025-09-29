from django.contrib import admin
from .models import Article, Comment, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "published_at")
    search_fields = ("title", "content", "author__username", "tags__name")
    list_filter = ("published_at",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "created_at")
    search_fields = ("content", "user__username")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
