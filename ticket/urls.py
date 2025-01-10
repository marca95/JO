from django.urls import path
from .views import ticket_view, offre_view

urlpatterns = [
  path('', ticket_view, name='ticket'),
  path('<int:sport_id>/events/', offre_view, name='ticket_events'),
]
