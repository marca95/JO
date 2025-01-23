from django.urls import path
from .views import panier, panier_check, status, personal_data, rgpd

urlpatterns = [
  path('', panier, name='panier'),
  path('checkout/', panier_check, name='panier_check'),
  path('status/', status, name='state'), 
  path('données_personnels/', personal_data, name='personal_data'), 
  path('reglement_general_protection_donnees/', rgpd, name='rgpd')
]
