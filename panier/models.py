from django.db import models
from django.contrib.auth.models import User

class Cart(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') 
  first_key = models.CharField(max_length=255, unique=True)
  second_key = models.DateTimeField(auto_now_add=True, null=True, blank=True)
