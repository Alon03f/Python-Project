from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet,
    CommentViewSet,
    TagViewSet,
    BookmarkListView,
    UserArticlesView
)

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
    path("bookmarks/", BookmarkListView.as_view(), name="bookmark_list"),
    path("users/<int:user_id>/articles/", UserArticlesView.as_view(), name="user_articles"),
]