from django.db import models
from django.core.validators import MinValueValidator
from panier.models import User

class Stadium(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=100, unique=True)
  available_space = models.IntegerField(validators=[MinValueValidator(0)])

class Sport(models.Model):
  name = models.CharField(max_length=50, unique=True)
  description = models.TextField()
  image = models.ImageField(unique=True)

class Nation(models.Model):
  name = models.CharField(max_length=50, unique=True)
  nickname = models.CharField(max_length=50, unique=True, blank=True)
  image = models.ImageField(unique=True)

class Event(models.Model):
  date = models.DateField()
  hour = models.TimeField()
  stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name='events')
  sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
  nation = models.ManyToManyField(Nation, related_name='events')
  admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  
class Player(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  birth_date = models.DateField()
  image = models.ImageField(default='players/default_image.jpg')
  events = models.ManyToManyField(Event, related_name='players')
  nation = models.ForeignKey(Nation, on_delete=models.CASCADE, related_name='players')
  sports = models.ManyToManyField(Sport, related_name='players')