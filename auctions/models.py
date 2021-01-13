from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass


# Watchlist
"""
User (Foreign key)
Listings (Foreign key)
"""

# auction listings
"""
User (foreign key)
active (active/inactive) bool
Title
Description
Starting-Bid
Image (URL)
Category (foreign key)
"""


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.ForeignKey("Category", on_delete=CASCADE, blank=True)

    def __str__(self):
        return f"{self.id}: {self.user} - {self.title}"


# auction categories
"""
Category
"""


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"


# bids
"""
User (foreign key)
Listing (foreign key)
Date
Bid
"""


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.bid} - {self.user} on listing [{self.listing}]"


# comments
"""
User (foreign key)
Listing (foreign key)
comments
"""