from django.forms import ModelForm, widgets
from django import forms


from .models import *

class CreateListingForm(forms.Form):
    title=forms.CharField(label="Title")
    description=forms.CharField(widget=forms.Textarea())
    image_url = forms.CharField(widget=forms.URLInput())
    BidPrice=forms.CharField(widget=forms.NumberInput())
