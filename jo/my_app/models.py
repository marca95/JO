from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
  name = models.CharField(max_length=50)
  first_name = models.CharField(max_length=50)
  email = models.EmailField(max_length=100, unique=True)
  password = models.CharField(max_length=255)
  
class Role(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.CharField(max_length=5, choices=[('admin', 'Admin'), ('user', 'User')])

class Stadium(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=100, unique=True)
  available_space = models.IntegerField()

class Cart(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') 
  first_key = models.CharField(max_length=255, unique=True)
  second_key = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Ticket(models.Model):
  qr_code = models.CharField(max_length=255, null=True, blank=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
  stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="tickets")
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="tickets")

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
  admin = models.ForeignKey(User)
  

