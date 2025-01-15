from django.urls import path
from .views import ticket_view, offre_view, detail_event

urlpatterns = [
  path('', ticket_view, name='ticket'),
  path('<str:sport_name>/events/', offre_view, name='ticket_events'),
  path('<str:sport_name>/events/<int:event_id>/', detail_event, name='detail_events'),
]
