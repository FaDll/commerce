from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.CreateListing,name="createlisting"),
    path("ListingDetails/<str:listing_id>",views.listings,name="ListingDetails"),
    path("bidding/<str:listing_id>",views.Bidding,name="bidding"),
    path("AddToWatchList/<str:listing_id>",views.AddToWatchList,name="AddToWatchList"),
    path("RemoveFromWatchList/<str:listing_id>",views.RemoveFromWatchList,name="RemoveFromWatchList"),
    path("WatchListPage",views.WatchListPage,name="WatchListPage"),
    path("Close_bidding/<str:listing_id>",views.Close_bidding,name="Close_bidding"),
    path("ItemsWon",views.ItemsWon,name="ItemsWon")

]
