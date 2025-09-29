from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment, Tag, ArticleLike, Bookmark
from .serializers import (
    ArticleListSerializer,
    ArticleWriteSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CommentDetailSerializer,
    TagSerializer,
    ArticleLikeSerializer,
    BookmarkSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsAuthenticatedOrReadOnly
from .filters import ArticleFilter


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for articles with advanced features"""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "excerpt", "tags__name", "author__username"]
    ordering_fields = ["published_at", "title", "views_count", "updated_at"]
    filterset_class = ArticleFilter
    
    def get_queryset(self):
        queryset = Article.objects.select_related("author", "author__profile").prefetch_related(
            "tags",
            Prefetch("likes", queryset=ArticleLike.objects.select_related("user")),
            Prefetch("bookmarks", queryset=Bookmark.objects.select_related("user"))
        )
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        if self.action == "list":
            queryset = queryset.annotate(
                likes_count=Count("likes", distinct=True),
                comments_count=Count("comments", distinct=True)
            )
        
        return queryset.order_by("-published_at")
    
    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminOrReadOnly()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ArticleWriteSerializer
        return ArticleDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve article and increment view count"""
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like an article"""
        article = self.get_object()
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        
        if not created:
            like.delete()
            return Response(
                {"message": "Article unliked", "is_liked": False},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"message": "Article liked", "is_liked": True},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        """Bookmark an article"""
        article = self.get_object()
        bookmark, created = Bookmark.objects.get_or_create(article=article, user=request.user)
        
        if not created:
            bookmark.delete()
            return Response(
                {"message": "Bookmark removed", "is_bookmarked": False},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {"message": "Article bookmarked", "is_bookmarked": True},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        """Get all comments for an article"""
        article = self.get_object()
        comments = article.comments.filter(parent=None).select_related("user", "user__profile").prefetch_related("replies")
        serializer = CommentDetailSerializer(comments, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        """Add a comment to an article"""
        article = self.get_object()
        serializer = CommentSerializer(
            data=request.data,
            context={"request": request, "article_id": article.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=["get"])
    def likes_list(self, request, pk=None):
        """Get list of users who liked the article"""
        article = self.get_object()
        likes = article.likes.select_related("user", "user__profile").order_by("-created_at")
        serializer = ArticleLikeSerializer(likes, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def popular(self, request):
        """Get popular articles by views"""
        articles = self.get_queryset().order_by("-views_count")[:10]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def trending(self, request):
        """Get trending articles by recent likes"""
        articles = self.get_queryset().annotate(
            recent_likes=Count("likes", filter=Q(likes__created_at__gte=timezone.now() - timezone.timedelta(days=7)))
        ).order_by("-recent_likes")[:10]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Comment.objects.select_related("user", "user__profile", "article").order_by("-created_at")
    
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticatedOrReadOnly()]
    
    def perform_destroy(self, instance):
        """Delete comment or its replies"""
        instance.delete()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for tags (read-only)"""
    queryset = Tag.objects.annotate(
        articles_count=Count("articles", filter=Q(articles__is_published=True))
    ).order_by("-articles_count")
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at", "articles_count"]
    
    @action(detail=True, methods=["get"])
    def articles(self, request, pk=None):
        """Get all articles for a specific tag"""
        tag = self.get_object()
        articles = tag.articles.filter(is_published=True).select_related(
            "author", "author__profile"
        ).prefetch_related("tags").order_by("-published_at")
        
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ArticleListSerializer(articles, many=True, context={"request": request})
        return Response(serializer.data)


class BookmarkListView(generics.ListAPIView):
    """List user's bookmarked articles"""
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related(
            "article", "article__author", "article__author__profile"
        ).prefetch_related("article__tags").order_by("-created_at")


class UserArticlesView(generics.ListAPIView):
    """List articles by a specific user"""
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        queryset = Article.objects.filter(author_id=user_id, is_published=True).select_related(
            "author", "author__profile"
        ).prefetch_related("tags").order_by("-published_at")
        return queryset


from django.utils import timezone