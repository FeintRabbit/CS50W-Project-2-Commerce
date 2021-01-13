from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Listing, User
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html")


@login_required
def test(request):
    return HttpResponse("test")


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


def listing(requst, listing_id):
    # query db for listing
    try:
        listing = Listing.objects.get(pk=listing_id)
        # send to page
        return HttpResponse(listing)

    except Listing.DoesNotExist:
        return redirect(reverse("index"))


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

            print(listing.id)

            return redirect("listing", listing_id=listing.id)

        else:
            render(request, "auctions/add_listing.html", {"form": form})
