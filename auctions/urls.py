from django.urls import path
from django.contrib import admin
from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("create_auction", views.create_auction_view, name="create_auction"),
    path("categories", views.categories_view, name="categories"),
    path("category/<str:category_name>", views.category_auctions_view, name="category_auctions"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("add_to_watchlist", views.add_to_watchlist_view, name="add_to_watchlist"),
    path("delete_from_watchlist", views.delete_from_watchlist_view, name="delete_from_watchlist"),
    path("auction/<str:auction_title>", views.auction_view, name="auction"),
    path("place_bid", views.place_bid_view, name="place_bid"),
    path("close_auction", views.close_auction_view, name="close_auction"),
    path("delete_auction", views.delete_auction_view, name="delete_auction"),
    path("create_comment", views.create_comment_view, name="create_comment"),
]