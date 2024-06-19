from django.urls import path

from .views import (
    RegisterView,
    UpdateProfileView,
    LoginView,
    LogoutPageView,
    LogoutView,
)

app_name = 'users'

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutPageView.as_view(), name="logout"),
    path("logout/commit/", LogoutView.as_view(), name="logout_commit"),
    path("update/", UpdateProfileView.as_view(), name="update")
]