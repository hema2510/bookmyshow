# movies/views.py

from django.shortcuts import render
from django.core.mail import send_mail
from .forms import BookingForm
from .models import Movie, Booking  # or whatever model holds your movies
from django.shortcuts import render, get_object_or_404
from .models import Movie, Theater
from django.shortcuts import render
from movies.models import Movie, Booking
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect, render, get_object_or_404
from .models import Booking

def confirm_booking(request):
    if request.method == 'POST':
        # Handle form, create booking as 'reserved'
        # ...
        booking = Booking.objects.create(
            user=request.user,
            theater=theater,
            # seats=selected_seats,
            status='reserved',
            reserved_at=timezone.now()
        )
        # Assign seats (many-to-many)
        booking.seats.set(selected_seats)
        booking.save()
        return redirect('payment_page', booking_id=booking.id)
    # else: show form

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Calculate time left
    now = timezone.now()
    time_left = max(0, int((booking.reserved_at + timedelta(minutes=2) - now).total_seconds()))
    if request.method == 'POST':
        # User clicked Pay Now
        if timezone.now() > booking.reserved_at + timedelta(minutes=2):
            booking.status = 'expired'
            booking.save()
            # Optionally, free seats here
            return render(request, 'payment_failed.html')
        else:
            booking.status = 'booked'
            booking.save()
            return render(request, 'payment_success.html')
    return render(request, 'payment.html', {'booking': booking, 'time_left': time_left})

# movies/views.py

from .models import Booking, Movie

def recommended_movies(request):
    recommended = Movie.objects.order_by('-rating')[:5]

    if request.user.is_authenticated:
        # Now use email to find bookings
        booked_names = Booking.objects.filter(email=request.user.email).values_list('movie', flat=True)
    recommendations = Movie.objects.exclude(name__in=booked_names).order_by('-rating')[:5]
    # fallback if none
    if not recommendations.exists():
        recommendations = Movie.objects.order_by('-rating')[:5]
    return render(request, 'movies/recommended.html', {'recommended_movies': recommendations})


def book_seats(request, theater_id):
    # Placeholder logic
    return render(request, 'movies/book_seats.html', {'theater_id': theater_id})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)  # or your related logic
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def book_ticket(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Send confirmation email
            send_mail(
                "Your BookMySeat Ticket Confirmation",
                f"Thank you for booking {booking.movie}!\nDetails: Theater: {booking.theater}, Time: {booking.show_time}, Seats: {booking.seats}.",
                None,  # Uses DEFAULT_FROM_EMAIL
                [booking.email],
            )
            return render(request, 'movies/booking_success.html', {'booking': booking})
    else:
        initial = {
            'movie': request.GET.get('movie', ''),
            'theater': request.GET.get('theater', ''),
            'show_time': request.GET.get('show_time', '')
        }
        form = BookingForm(initial=initial)
    return render(request, 'movies/booking_page.html', {'form': form})
    
