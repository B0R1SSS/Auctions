from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import RegisteredUser, Auction, Bid, Comment, Category


def index_view(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = RegisteredUser.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    elif request.method == "GET":
        return render(request, "auctions/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    elif request.method == "GET":
        return render(request, "auctions/login.html")


@login_required(login_url="auctions:login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def get_category(category_name):
    if not category_name:
        return None
    category = Category.objects.filter(name=category_name).first()
    if not category:
        category = Category(name=category_name)
        category.save()
    return category

@login_required(login_url="auctions:login")
def create_auction_view(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        user = request.user
        category_name = request.POST["category_name"]
        category = get_category(category_name)
        if request.POST["image_url"]:
            image_url = request.POST["image_url"]
        else:
            image_url = "https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg"
        auction = Auction(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, user=user)
        auction.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    return render(request, "auctions/create_auction.html")


def categories_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
            "categories": categories
        })


def category_auctions_view(request, category_name):
    if request.method == "GET":
        category = Category.objects.get(name=category_name)
        category_auctions = Auction.objects.filter(category=category)
        return render(request, "auctions/index.html", {
        "auctions": category_auctions
    })


@login_required(login_url="auctions:login")
def watchlist_view(request):
    if request.method == "GET":
        user = request.user
        watchlist_auctions = user.watchlist_auctions.all()
        return render(request, "auctions/index.html", {
            "auctions": watchlist_auctions
        })


@login_required(login_url="auctions:login")
def add_to_watchlist_view(request):
    if request.method == "POST":
        auction = Auction.objects.get(title=request.POST["auction_title"])
        user = request.user
        auction.watchlist.add(user)
        auction.save()
        return HttpResponseRedirect(reverse("auctions:watchlist"))


@login_required(login_url="auctions:login")
def delete_from_watchlist_view(request):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(title=request.POST["auction_title"])
        user.watchlist_auctions.remove(auction)
        user.save()
        return HttpResponseRedirect(reverse("auctions:watchlist"))


def auction_view(request, auction_title):
    if request.method == "GET":
        auction = Auction.objects.get(title=auction_title)
        comments = auction.comments.all()
        heighest_bid = auction.heighest_bid
        if heighest_bid:
            min_next_bid_value = heighest_bid.value + 0.01
        else:
            min_next_bid_value = auction.starting_bid
        return render(request, "auctions/auction.html", {
            "auction": auction,
            "heighest_bid": heighest_bid,
            "min_next_bid_value": min_next_bid_value,
            "comments": comments
        })


@login_required(login_url="auctions:login")
def place_bid_view(request):
    if request.method == "POST":
        auction = Auction.objects.get(title=request.POST["auction_title"])
        bid_value = request.POST["bid_value"]
        new_bid = Bid(value=bid_value, auction=auction, user=request.user)
        auction.heighest_bid = new_bid
        new_bid.save()
        auction.save()
        return HttpResponseRedirect(reverse("auctions:auction", args=(auction.title,)))


@login_required(login_url="auctions:login")
def close_auction_view(request):
    if request.method == "POST":
        auction_title = request.POST["auction_title"]
        auction = Auction.objects.get(title=auction_title)
        creator = request.user
        winning_bid = Bid.objects.get(auction=auction)
        winner = winning_bid.user
        auction.delete()
        return render(request, "auctions/index.html", {
            "message": f"Auction of {auction.title} was closed with winner {winner.username}",
            "auctions": Auction.objects.all()
        })


@login_required(login_url="auctions:login")
def delete_auction_view(request):
    if request.method == "POST":
        auction_title = request.POST["auction_title"]
        auction = Auction.objects.get(title=auction_title)
        creator = request.user
        auction.delete()
        return render(request, "auctions/index.html", {
            "message": f"Auction of {auction_title} was deleted with no winner",
            "auctions": Auction.objects.all()
        })


@login_required(login_url="auctions:login")
def create_comment_view(request):
    if request.method == "POST":
        auction = Auction.objects.get(title=request.POST["auction_title"])
        comment_content = request.POST["comment_content"]
        comment = Comment(content=comment_content, auction=auction, user=request.user)
        comment.save()
        return HttpResponseRedirect(reverse("auctions:auction", args=(auction.title,)))
