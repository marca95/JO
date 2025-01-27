from django.test import TestCase
from django.urls import reverse, resolve
from sports.views import *

# urlpatterns = [
#   path('', home, name='home'),
#   path('<str:sport_name>/events/', sport_events, name='sport_events'),
# ]


class testUrls(TestCase):
  def test_url_home(self):
    url = reverse('home')
    self.assertEqual(resolve(url).func, home)
    
  def test_sports_events_url(self):
    sport_name = 'Basket'
    url = reverse('sport_events', args=[sport_name])
    self.assertEqual(resolve(url).func, sport_events)
    
  def test_home_url_status_code(self):
    response = self.client.get(reverse('home')) 
    self.assertEqual(response.status_code, 200)  

  def test_sport_events_url_status_code(self):
    valid_sports = ['Football', 'Basket']
    sport_name = "Football"
    if sport_name not in valid_sports :
      response = self.client.get(reverse('sport_events', args=[sport_name]))  
      self.assertEqual(response.status_code, 200)  

  def test_sport_events_url_not_found(self):
    valid_sports = ['Football', 'Basket']
    sport_name = "Football"
    if sport_name not in valid_sports :
      response = self.client.get('/toto/events/')  
      self.assertEqual(response.status_code, 404)  