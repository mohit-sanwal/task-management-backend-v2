from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    CurrentUserView,
    UpdateUserRoleView,
    DeleteUserView,
    UserListView,
)

urlpatterns = [
    path("register", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("current-user", CurrentUserView.as_view()),
    path("users", UserListView.as_view()),

    path(
        "users/<int:user_id>/role",
        UpdateUserRoleView.as_view()
    ),

    path(
        "users/<int:user_id>",
        DeleteUserView.as_view()
    ),
]


