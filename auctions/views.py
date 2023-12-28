from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listing,Bids,Watchlist,Comment

def isOwner(user, listing):
    isowner = False
    if user == listing.owner:
        isowner = True
    return isowner

def isWishlist(user,listing):
    iswishlist = False
    try:
        wishlist = Watchlist.objects.get(owner=user,listing=listing)
        iswishlist = wishlist.isWishlist
    except:
        wishlist = None
    return iswishlist

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings
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


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["min_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["category"]
        if category=="No category":
            category_of_object = None
        else:
            category_of_object = Category.objects.get(category=category)
        
        owner = request.user

        new_listing = Listing(
            title=title,
            description=description,
            min_bid=float(bid),
            max_bid=float(bid),
            image_url=image_url,
            category=category_of_object,
            owner=owner
        )
        try:
            new_listing.save()
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Couldn't create new listing"
            })
        
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html",{
            "categories": categories
        })
        
def listing(request, title):
    listing = Listing.objects.get(title=title)
    user = request.user
    comments = Comment.objects.filter(listing=listing)
    iswishlist = isWishlist(user,listing)
    isowner = isOwner(user,listing)

    if listing.active:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "isOwner": isowner,
            "wishlist": iswishlist,
            "comments": comments
        })
    else:
        bidder = Bids.objects.filter(listing=listing).last()
        if bidder:
            if bidder.bidder == user and not isowner:
                winner = True
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "isOwner": isowner,
                    "winner": winner,
                    "wishlist": iswishlist,
                    "comments": comments
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "isOwner": isowner,
                    "wishlist": iswishlist,
                    "comments": comments
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "isOwner": isowner,
                "wishlist": iswishlist,
                "comments": comments    
            })
    
    

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=Category.objects.get(category=category))
    
    return render(request, "auctions/listing_by_category.html",{
        "listings": listings
    })

def bid(request, title):
    listing = Listing.objects.get(title=title)
    comments = Comment.objects.filter(listing=listing)
    if request.method == "POST":
        bid = request.POST["bid"]
        isAlert = False
        user = request.user
        isowner = isOwner(user,listing)
        iswishlist = isWishlist(user,listing)
        if float(bid) > listing.min_bid and float(bid) > listing.max_bid:
            current_user = request.user
            listing.max_bid = bid
            try:
                listing.save()
            except:
                return 
                
            new_bid = Bids(
                bid=bid,
                listing=listing,
                bidder=current_user
            )
            try:
                new_bid.save()
            except:
                return
            congrat = True
            
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "isAlert": isAlert,
                "congrat": congrat,
                "wishlist": iswishlist,
                "comments": comments
            })
        else:
            isAlert = True
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "isOwner": isowner,
                "isAlert": isAlert,
                "wishlist": iswishlist,
                "comments": comments
            })

def close_listing(request, title):
    if request.method == "POST":

        listing = Listing.objects.get(title=title)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
def add_wishlist(request, title):
    listing = Listing.objects.get(title=title)
    user = request.user
    comments = Comment.objects.filter(listing=listing)
    try:
        wishlist = Watchlist.objects.get(owner=user,listing=listing)
    except:
        wishlist = None
    if wishlist == None:
        new_wishlist= Watchlist(
            isWishlist = True,
            listing = listing,
            owner = user
        )
        new_wishlist.save()
    else:
        wishlist.isWishlist = True
        wishlist.save()
    isowner = isOwner(user,listing)
    return render(request, "auctions/listing.html",{
                "listing": listing,
                "isOwner": isowner,
                "wishlist": True,
                "comments": comments
            })
    
def remove_wishlist(request, title):
    listing = Listing.objects.get(title=title)
    user = request.user
    comments = Comment.objects.filter(listing=listing)
    wishlist = Watchlist.objects.get(owner=user,listing=listing)
    wishlist.isWishlist = False
    wishlist.save()
    isowner = isOwner(user,listing)
    iswishlist = isWishlist(user, listing)
    return render(request, "auctions/listing.html",{
                "listing": listing,
                "isOwner": isowner,
                "wishlist": iswishlist,
                "comments": comments
            })

def wishlists(request):
    user = request.user
    wishlists = Watchlist.objects.filter(isWishlist=True,owner=user)
    return render(request, "auctions/wishlists.html", {
        "wishlists": wishlists
    })

def comment(request, title):
    listing = Listing.objects.get(title=title)
    user = request.user
    
    isowner = isOwner(user,listing)
    iswishlist = isWishlist(user,listing)
    if request.method == "POST":
        text = request.POST["comment"]
        new_comment = Comment(
            text=text,
            listing=listing,
            owner=user
        )
        try:
            new_comment.save()
        except:
            return
        comments = Comment.objects.filter(listing=listing)
        return render(request, "auctions/listing.html",{
                "listing": listing,
                "isOwner": isowner,
                "wishlist": iswishlist,
                "comments": comments
            })
