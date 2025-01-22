from django.urls import path
from .views import panier, panier_check, mock_payment, status

urlpatterns = [
  path('', panier, name='panier'),
  path('checkout/', panier_check, name='panier_check'),
  path('status/', status, name='state')
]
