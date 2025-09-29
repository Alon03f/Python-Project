from rest_framework import viewsets, permissions, generics, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Article, Comment
from .serializers import (
    ArticleListSerializer,
    ArticleWriteSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("author").prefetch_related("tags").order_by("-published_at")
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "content", "tags__name", "author__username"]
    ordering_fields = ["published_at", "title"]
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

class ArticleCommentsListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    def get_queryset(self):
        return Comment.objects.filter(article_id=self.kwargs["pk"]).select_related("user").order_by("-created_at")
    def create(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs["pk"])
        serializer = self.get_serializer(data=request.data, context={"request": request, "article": article})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = {"Location": ""}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommentDestroyUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.select_related("user", "article")
    serializer_class = CommentSerializer
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        return [permissions.AllowAny()]
