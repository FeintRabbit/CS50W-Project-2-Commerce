from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Bid, Listing, User, Watchlist
from .forms import ListingForm

####################
# App views
####################


def index(request):
    # get active listings
    listings = Listing.objects.filter(active=True)

    for i, listing in enumerate(listings):
        if not listing.bids.all():
            listings[i].current_bid = listings[i].start_bid
        else:
            max_bid = listing.bids.all().aggregate(Max("bid"))["bid__max"]
            listings[i].current_bid = format(float(max_bid), ".2f")

    return render(request, "auctions/index.html", {"listings": listings})


def listing(request, listing_id):
    if request.method == "GET":
        try:
            # listing context
            listing = Listing.objects.get(pk=listing_id)

            if not listing.bids.all():
                listing.current_bid = listing.start_bid
            else:
                max_bid = listing.bids.all().aggregate(Max("bid"))["bid__max"]
                listing.current_bid = format(float(max_bid), ".2f")

            # watchlist context
            check_watchlist = Watchlist.objects.filter(user__exact=request.user).filter(
                listing__exact=listing
            )

            # listing comments context TODO

            # error message from post attempt
            error_message = None
            if "error_message" in request.session:
                error_message = request.session["error_message"]
                del request.session["error_message"]

            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": listing,
                    "check_watchlist": check_watchlist,
                    "error_message": error_message,
                },
            )

        except Listing.DoesNotExist:
            return redirect(reverse("index"))

    # post for new bids
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        bid = float(request.POST["bid"])

        if not listing.bids.all():
            if bid >= listing.start_bid:
                new_bid = Bid(user=request.user, listing=listing, bid=bid)
                new_bid.save()
            else:
                request.session[
                    "error_message"
                ] = "Bid must be equal to or higher than start bid"
        else:
            max_bid = listing.bids.all().aggregate(Max("bid"))["bid__max"]
            if bid > max_bid:
                new_bid = Bid(user=request.user, listing=listing, bid=bid)
                new_bid.save()
            else:
                request.session["error_message"] = "Bid must be higher than current bid"

        return redirect("listing", listing_id=listing_id)


def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST["listing"]
        listing = Listing.objects.get(pk=listing_id)

        # checks if listing in users watchlist
        check_watchlist = Watchlist.objects.filter(user__exact=request.user).filter(
            listing__exact=listing
        )
        if check_watchlist:
            check_watchlist.delete()
        else:
            watchlist = Watchlist(user=request.user, listing=listing)
            watchlist.save()

        return redirect("listing", listing_id=listing_id)


@login_required
def add_listing(request):
    if request.method == "GET":
        form = ListingForm()

        return render(request, "auctions/add_listing.html", {"form": form})

    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]

            listing = Listing(
                user=user,
                title=title,
                description=description,
                start_bid=start_bid,
                image=image,
                category=category,
            )

            listing.save()

            return redirect("listing", listing_id=listing.id)

        else:
            render(request, "auctions/add_listing.html", {"form": form})


####################
# Authentication
####################


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
