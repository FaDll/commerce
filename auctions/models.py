from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
from commerce.settings import TIME_ZONE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listing(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userlistings")
    title=models.CharField(max_length=64)
    description= models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    image_url = models.URLField(default='google.com')
    #currentdate= models.DateField(default=TIME_ZONE)
    sold=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} posted by {self.userid}"
        
class Bid(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    listing=models.ForeignKey(listing,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"bid on item: {self.listing} by {self.userid} with price: {self.price}"

class WatchList(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userwatchlist")
    ListingID=models.ManyToManyField(listing,related_name="listings")
    watching=models.BooleanField(default=False)

class comment(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE,related_name="usercomment")
    listingID=models.ForeignKey(listing,on_delete=models.CASCADE)
    comment=models.TextField()

class Winner(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingID=models.ForeignKey(listing,on_delete=models.CASCADE)

    def __str__(self):
        return f"winner is : {self.winner}"