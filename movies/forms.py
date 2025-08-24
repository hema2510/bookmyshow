from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'movie', 'theater', 'show_time', 'seats']  # Use your actual Booking model fields here