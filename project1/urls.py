from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("signup", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("library", views.library, name="library"),
    path("book_detail", views.book_detail, name="book_detail"),
    path("logout", views.logout_view, name="logout"),
]