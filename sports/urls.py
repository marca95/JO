from django.urls import path
from .views import home, sport_events

urlpatterns = [
  path('', home, name='home'),
  path('<str:sport_name>/events/', sport_events, name='sport_events'),
]
