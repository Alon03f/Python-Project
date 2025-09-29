from django.urls import path
from .views import (
    RegisterAPIView,
    MeAPIView,
    ChangePasswordAPIView,
    UserDetailAPIView,
    UserListAPIView
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("me/", MeAPIView.as_view(), name="me"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
]