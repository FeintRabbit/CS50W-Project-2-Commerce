from django.forms import ModelForm
from auctions.models import Listing


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "category", "start_bid", "image", "description"]

        labels = {
            "start_bid": ("Start bid ($)"),
            "image": ("Link to image"),
        }
