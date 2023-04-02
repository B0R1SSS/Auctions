from django.contrib import admin
from .models import RegisteredUser, Auction, Bid, Comment, Category


admin.site.register(RegisteredUser)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)