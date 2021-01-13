from django.contrib.auth.models import AbstractUser
from django.db import models


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
Status (active/inactive) bool
Title
Description
Starting-Bid
Image (URL)
Category (foreign key)
"""

# auction categories
"""
Category
"""

# bids
"""
User (foreign key)
Listing (foreign key)
Date
Bid
"""

# comments
"""
User (foreign key)
Listing (foreign key)
comments
"""