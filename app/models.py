from pyexpat import model
from django.db import models

# Create your models here.
class Movie(models.Model):
    hall = models.CharField(max_length=20)
    movie = models.CharField(max_length=20)
    def __str__(self):
        return self.movie

class Guest(models.Model):
    name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    guest = models.ForeignKey(Guest,on_delete=models.CASCADE, related_name='reservation' )
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE, related_name='reservation' )
    def __str__(self):
        return self.guest.name
    