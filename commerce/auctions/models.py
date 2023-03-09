from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.id}- {self.username}"


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", blank=True)
    auctionListing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.id}"


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)
    image = models.CharField(max_length=16384, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="category", blank= True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    listedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}- {self.title}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comment", blank=True, null=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comment")

    def __str__(self):
        return f"{self.message}"

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="price")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")
    price = models.FloatField(unique=True)
    modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.price}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"

class Activities(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="logListing")
    bidUpdate = models.DateTimeField(null=True, blank=True)
    closeUpdate = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="logUser")
    comment = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, related_name="logComment", null=True, blank=True)
    commentUpdate = models.DateTimeField(null=True, blank=True)


class Winners(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="winner")
    happens = models.DateTimeField(auto_now_add=True)