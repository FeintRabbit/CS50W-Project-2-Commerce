from django.contrib import admin

from .models import User, Listing, Category, Bid, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Watchlist)
