from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentDestroyView

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"comments", CommentDestroyView, basename="comment")

urlpatterns = [path("", include(router.urls))]
