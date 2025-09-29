from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Comment, Tag, ArticleLike, Bookmark


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "is_published", "views_count", "published_at", "likes_count")
    list_filter = ("is_published", "published_at", "tags")
    search_fields = ("title", "content", "author__username", "tags__name")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views_count", "published_at", "updated_at", "slug")
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    list_per_page = 20
    
    fieldsets = (
        ("Article Information", {
            "fields": ("title", "slug", "author", "content", "excerpt", "featured_image")
        }),
        ("Publishing", {
            "fields": ("is_published", "tags")
        }),
        ("Statistics", {
            "fields": ("views_count", "published_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def likes_count(self, obj):
        count = obj.likes.count()
        return format_html('<strong>{}</strong>', count)
    likes_count.short_description = "Likes"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author").prefetch_related("tags", "likes")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "content_preview", "is_edited", "created_at")
    list_filter = ("is_edited", "created_at")
    search_fields = ("content", "user__username", "article__title")
    readonly_fields = ("created_at", "updated_at", "is_edited")
    date_hierarchy = "created_at"
    list_per_page = 20
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "article")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "articles_count", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)
    
    def articles_count(self, obj):
        count = obj.articles.filter(is_published=True).count()
        return format_html('<strong>{}</strong>', count)
    articles_count.short_description = "Articles"


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "article")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "article", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "article__title")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "article")