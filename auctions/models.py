from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=32)
    min_bid = models.FloatField()
    max_bid = models.FloatField()
    image_url = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name="categoryoflisting")
    active = models.BooleanField(default = True)
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name="owner")

    def __str__(self):
        return f"{self.title}"

class Bids(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True,null=True,related_name="related_listing")
    bidder = models.ForeignKey(User,  on_delete=models.CASCADE,null=True,blank=True, related_name="bidder")

    def __str__(self):
        return f"{self.bid}"
    
class Watchlist(models.Model):
    isWishlist = models.BooleanField(default=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True,null=True,related_name="wished_listing")
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name="owner_of_wishlist")

    def __str__(self):
        return f"{self.listing.title} and {self.owner.username}"
    
class Comment(models.Model):
    text = models.CharField(max_length=32)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True,null=True,related_name="comment_listing")
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE,related_name="owner_of_comment")
    def __str__(self):
        return f"Comment in {self.listing.title} and comment of {self.owner.username}, he said {self.text}"