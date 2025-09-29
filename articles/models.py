from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from blog_api.utils import sanitize_html


class Tag(models.Model):
    """Tag model for categorizing articles"""
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class Article(models.Model):
    """Article model with enhanced features"""
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3, "Title must be at least 3 characters long")]
    )
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    content = models.TextField(
        validators=[MinLengthValidator(10, "Content must be at least 10 characters long")]
    )
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short summary of the article")
    featured_image = models.ImageField(upload_to="articles/", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)
    is_published = models.BooleanField(default=True, help_text="Is this article visible to the public?")
    views_count = models.PositiveIntegerField(default=0, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        self.content = sanitize_html(self.content)
        
        if not self.excerpt:
            self.excerpt = self.content[:297] + "..." if len(self.content) > 300 else self.content
        
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Increment article view count"""
        self.views_count += 1
        self.save(update_fields=["views_count"])
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["slug"]),
        ]


class Comment(models.Model):
    """Comment model with enhanced features"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(
        validators=[MinLengthValidator(2, "Comment must be at least 2 characters long")]
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.content = sanitize_html(self.content)
        if self.pk:
            self.is_edited = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} on {self.article.title}"
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]


class ArticleLike(models.Model):
    """Like system for articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("article", "user")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"


class Bookmark(models.Model):
    """Bookmark system for saving articles"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("article", "user")
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"