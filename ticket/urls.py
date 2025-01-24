from django.urls import path
from .views import ticket_view, offre_view, detail_view

urlpatterns = [
  path('', ticket_view, name='ticket'),
  path('<str:sport_name>/events/<int:event_id>/', detail_view, name='ticket_detail'),
  path('<str:sport_name>/', offre_view, name='ticket_events'),
]
