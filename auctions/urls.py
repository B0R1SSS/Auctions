from django.urls import path
from django.contrib import admin
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("admin_interface", admin.site.urls, name="admin_interface")
]