from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'movie', 'theater', 'show_time', 'seats', 'booked_at']