from django.db import models
from django.contrib.auth.models import User
from ticket.models import Ticket

class Cart(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') 
  first_key = models.CharField(max_length=255)
  second_key = models.CharField(max_length=255, null=True, blank=True)
  tickets = models.ManyToManyField(Ticket, related_name='carts')
