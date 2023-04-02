from django.urls import path
from django.contrib import admin
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
]