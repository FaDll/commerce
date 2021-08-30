from auctions.forms import CreateListingForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):

    listings=listing.objects.filter(sold=False)

    return render(request, "auctions/index.html",{
        "listings":listings
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


@login_required
def CreateListing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["BidPrice"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            listing.objects.create(userid = user, title = title, description = description, 
            price = bid,image_url = image_url)
    
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/createlisting.html", {
            "listing_form": CreateListingForm()
        })            
    
@login_required
def listings(request,listing_id):
        Listing= listing.objects.get(pk=listing_id)
        user=request.user
        #watch=WatchList.objects.filter(userID=user,ListingID=Listing)
        #if watch:
        #    watchingornot=WatchList.objects.get(userID = user, ListingID = Listing).watching
        #else:
         #   watchingornot=None
        watchingornot=checkWatching(WatchList,Listing,user)
        return render(request,"auctions/ListingDetails.html",{
            "listing":Listing,
            "watching": watchingornot,
            'owner':user
    })

def Bidding(request,listing_id):

    if request.method == 'POST':
        Listing=listing.objects.get(pk=listing_id)
        user=request.user
        bid=request.POST['bid']
        Listing.price=bid
        Listing.save()
        #watching=WatchList.objects.get(userID=user,ListingID=Listing).values('watching')
        Bid.objects.create(userid=user,listing=Listing,price=bid)

    
    return render(request,"auctions/ListingDetails.html",{
        "listing":Listing
        #"watching":watching
    })

def AddToWatchList(request,listing_id):

    Listing=listing.objects.get(pk=listing_id)
    user=request.user
    #watch=WatchList.objects.filter(userID=user,ListingID=Listing)
    #if watch:
    #    watch=WatchList.objects.get(userID=user,ListingID=Listing)
    #    watch.watching=True
    #    watch.save()
    #else:
      #  WatchList.objects.create(userID = user,watching = True)
      #  WatchList.ListingID.set(Listing)
    watchlistobj=WatchList.objects.create(userID=user,watching=True)
    watchlistobj.ListingID.add(Listing)
    watchingornot=checkWatching(WatchList,Listing,user)

    return render(request,"auctions/ListingDetails.html", {
        "listing": Listing,
        "watching":watchingornot
    })

def RemoveFromWatchList(request,listing_id):
    Listing=listing.objects.get(pk=listing_id)
    user=request.user
    WatchList.objects.filter(ListingID=Listing,userID=user).delete()
    
    watchingornot=checkWatching(WatchList,Listing,user)
    return render(request,"auctions/ListingDetails.html",{
        "listing":Listing,
        "watching": watchingornot
    })

def WatchListPage(request):
    AllWatchListsIDs=WatchList.objects.filter(userID=request.user).values('ListingID')
    AllListsIDs=listing.objects.filter(pk__in=AllWatchListsIDs)
    return render(request,"auctions/WatchList.html",{
        "AllItems":AllListsIDs
    })
def Close_bidding(request,listing_id):
    winobj = Winner()
    listingItemWon=listing.objects.get(pk=listing_id)
    listingItemWon.sold=True
    listingItemWon.save()
    winner = Bid.objects.get(price = listingItemWon.price, listing = listingItemWon)
    winobj.owner=request.user
    winobj.winner=winner.userid
    winobj.listingID=listingItemWon
    winobj.save()
    return render(request,"auctions/ListingDetails.html", {
        "listing": listingItemWon,
    })


def ItemsWon(request):

   user=request.user
   winners=Winner.objects.filter(winner=user)
   return render(request,"auctions/ItemsWon.html",{
       "Wonitems":winners,
   }) 

def checkWatching(WatchList, listing,watchedby):
    watching = WatchList.objects.filter(userID=watchedby, ListingID=listing).count()
    if (watching > 0):
        return True
    else:
        return False
