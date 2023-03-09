from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count, Max
from datetime import datetime

from .models import User, AuctionListing, Comment as MComment, Bids, Category, Watchlist, Activities, Winners


def index(request, user_lists=""):
    if user_lists:
        activeListings = User.objects.get(pk=user_lists).creator.all()
        message = User.objects.get(pk=user_lists).username
    else:
        activeListings = AuctionListing.objects.filter(active=True)
        message = None
    try:
        watchlist = Watchlist.objects.filter(user=request.user).count()
    except:
        watchlist = None
    return render(request, "auctions/index.html", {
        "watchlist": watchlist,
        "page": "ActiveListings",
        "activeListings": activeListings,
        "message": message,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Validation
        if username == "" or password == "" or confirmation == "":
            return render(request, "auctions/register.html", {
                "message": "Fill data."
            })

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateListing(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", max_length=65536)
    bidStarting = forms.FloatField(
        label="Starting Bid", 
        min_value=0,
        widget=forms.TextInput(attrs={'placeholder': 'Dollars'})
    )
    image = forms.CharField(label="Image URL", required=False, max_length=16384)
    category = forms.ModelChoiceField(label="Category", required=False, queryset=Category.objects.all())

@login_required(redirect_field_name="request", login_url="login")
def createListing(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            listedBy = request.user 
            price = form.cleaned_data["bidStarting"]
            a = AuctionListing(title=title, description=description, image=image, category=category, listedBy=listedBy)
            a.save()

            user = request.user
            b = Bids(listing=a, user=user, price=price)
            b.save()

        else:
            return render(request, "auctions/index.html",{
                'page': 'CreateListing',
                "watchlist": Watchlist.objects.filter(user=request.user).count(),
                'form': form
            })

    return render(request, "auctions/index.html", {
        "page": "CreateListing",
        "watchlist": Watchlist.objects.filter(user=request.user).count(),
        "form": CreateListing()
    })

class PlaceBid(forms.Form):
    price = forms.FloatField(
    label="", 
    min_value=0,
    widget=forms.TextInput(attrs={'placeholder': 'Bid', 'class': "listing_bid"})
    )
class Comment(forms.Form):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={
        'placeholder': 'Comment', 'class': 'listing_textarera'
    }))

def listingPage(request, auction_id):
    frmValid = True
    notice=""
    listing = AuctionListing.objects.get(pk=auction_id)
    try:
        news = Winners.objects.get(listing=listing)
    except:
        news = None
    try:
        activities = Activities.objects.filter(listing=listing)
    except:
        activities = None
    try:
        watchlist = Watchlist.objects.filter(user=request.user).count()
    except:
        watchlist = None
    whatchlisted = listing.listing.first()
    bids = listing.price.all()
    comments = listing.comment.all()
    form = PlaceBid(request.POST)
    if request.method == "POST":
        frmValid = False
        if form.is_valid():
            price = form.cleaned_data["price"]
            if price > bids.aggregate(Max('price'))["price__max"]:
                frmValid = True
                b = Bids(listing=listing, user=request.user, price=price)
                b.save()
            else:
                notice = "(The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).)"
    return render(request, "auctions/index.html", {
        "page": "ListingPage",
        "watchlist": watchlist,
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "form": PlaceBid() if frmValid else form,
        "notice": notice,
        "whatchlisted": whatchlisted,
        "activities": activities,
        "news": news,
        "commentForm": Comment()
    })

def whatchlisting(request, auction_id, sit):
    listing = AuctionListing.objects.get(pk=auction_id)
    if sit == "add":
        w = Watchlist(auctionListing=listing, user=request.user)
        w.save()
    elif sit == "remove":
        w = listing.listing.first()
        w.delete()
    return HttpResponseRedirect(reverse("listing", args=(auction_id,)))

def close(request, auction_id):
    AuctionListing.objects.filter(pk=auction_id).update(active=False)
    listing = AuctionListing.objects.get(pk=auction_id)
    a = Activities(listing=listing, user=request.user, closeUpdate=datetime.now())
    a.save()
    winner = listing.price.get(price=listing.price.all().aggregate(Max('price'))["price__max"]).user
    w = Winners(user=winner, listing=listing)
    w.save()
    return HttpResponseRedirect(reverse("listing", args=(auction_id,)))


def comment (request, auction_id):
    listing = AuctionListing.objects.get(pk=auction_id)
    if request.method == "POST":
        commentForm = Comment(request.POST)
        if commentForm.is_valid():
            message = commentForm.cleaned_data["comment"]
            commentForm = Comment()
            c = MComment(message=message, user=request.user, listing=listing)
            c.save()
        else:
            return render(request, "auctions/index.html", {
                "page": "ListingPage",
                "listing": listing,
                "bids": listing.price.all(),
                "comments": listing.comment.all(),
                "commentForm": commentForm
            })
    return HttpResponseRedirect(reverse("listing", args=(auction_id,)))



@login_required(redirect_field_name="request", login_url="login")
def categories(request, id):
    if id:
        items = Category.objects.get(pk=id).category.all()
    else:
        items = Category.objects.all()
    return render(request, "auctions/index.html", {
        "page": "Categories",
        "watchlist": Watchlist.objects.filter(user=request.user).count(),
        "categories": items,
        "id": id,
    })


@login_required(redirect_field_name="request", login_url="login")
def watchlist(request):
    return render(request, "auctions/index.html", {
        "page": "Watchlist",
        "watchlist": Watchlist.objects.filter(user=request.user).count(),
        "watchlists": request.user.watchlist.all(),
    })