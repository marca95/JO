from django.db import models
from panier.models import User
from sports.models import Event
from panier.models import Cart
from django.core.validators import MinValueValidator

class Ticket(models.Model):
  price = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0)])
  formula = models.CharField(max_length=100, null=True)
  qr_code = models.ImageField(max_length=255, null=True, blank=True)
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets", null=True, blank=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="tickets", null=True, blank=True)