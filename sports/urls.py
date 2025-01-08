from django.urls import path
from .views import home, sport_events

urlpatterns = [
  path('', home, name='home'),
  path('sport/<int:sport_id>/events/', sport_events, name='sport_events'),  # Nouvelle URL pour les événements
]
