from django.db import models
from django.contrib.auth.models import AbstractUser


class RegisteredUser(AbstractUser):
    def __str__(self):
        return f"User {self.id}: {self.username}"


class Category(models.Model):
    name =  models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name="bids")
    value = models.FloatField()

    def __str__(self):
        return f"Bid ${self.value} placed by {self.user}"


class Auction(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name="owned_auctions", default=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="auctions", null=True)
    heighest_bid = models.OneToOneField(Bid, on_delete=models.SET_NULL, related_name="auction", null=True)
    watchlist = models.ManyToManyField(RegisteredUser, related_name="watchlist_auctions")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=True)
    starting_bid = models.FloatField()
    image_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Auction: {self.title}"


class Comment(models.Model):
    user = models.ForeignKey(RegisteredUser, on_delete=models.DO_NOTHING, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"Comment on {self.auction.title} by {self.user}"

