from django.test import TestCase
from django.urls import reverse, resolve
from ticket.views import ticket_view, offre_view, detail_view


# urlpatterns = [
#   path('', ticket_view, name='ticket'),
#   path('<str:sport_name>/events/<int:event_id>/', detail_view, name='ticket_detail'),
#   path('<str:sport_name>/', offre_view, name='ticket_events'),
# ]


class TestTicketUrls(TestCase):
  def test_ticket_url_resolves(self):
    url = reverse('ticket')  
    self.assertEqual(resolve(url).func, ticket_view) 

  def test_ticket_events_url_resolves(self):
    url = reverse('ticket_events', args=['Football'])  
    self.assertEqual(resolve(url).func, offre_view)  
        
  def test_ticket_detail_url_resolves(self):
    url = reverse('ticket_detail', args=['Football', 1]) 
    self.assertEqual(resolve(url).func, detail_view) 
    
  def test_ticket_view_status_code(self):
    response = self.client.get(reverse('ticket')) 
    self.assertEqual(response.status_code, 200)  

  def test_offre_view_status_code(self):
    response = self.client.get(reverse('ticket_events', args=['Football']))  
    self.assertEqual(response.status_code, 200) 

  def test_detail_view_status_code(self):
    response = self.client.get(reverse('ticket_detail', args=['Football', 1]))  
    self.assertEqual(response.status_code, 200)  
