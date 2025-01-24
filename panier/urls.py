from django.urls import path
from .views import *

urlpatterns = [
  path('', panier, name='panier'),
  path('checkout/', panier_check, name='panier_check'),
  path('status/', status, name='state'), 
  path('données_personnels/', personal_data, name='personal_data'), 
  path('reglement_general_protection_donnees/', rgpd, name='rgpd'),
  path('mentions_legales/', mentions, name='mentions'),
  path('cgv/', cgv, name='cgv'),
  path('cgu/', cgu, name='cgu')
]
