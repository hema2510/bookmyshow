from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone

STATUS_CHOICES = (
    ('reserved', 'Reserved'),
    ('booked', 'Booked'),
    ('expired', 'Expired'),
)

class Movie(models.Model):
    name= models.CharField(max_length=255)
    image= models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3,decimal_places=1)
    cast= models.TextField()
    description= models.TextField(blank=True,null=True) # optional

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='theaters')
    time= models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default='test@example.com')
    movie = models.CharField(max_length=100)
    theater = models.CharField(max_length=100)
    show_time = models.CharField(max_length=50)
    seats = models.CharField(max_length=100)
    booked_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.name} - {self.movie} @ {self.show_time}"
    
    