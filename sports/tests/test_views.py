from django.test import TestCase
from django.urls import reverse
from sports.views import *

class TestHomeView(TestCase):
  def test_home_uses_correct_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')
    
  def test_home_context(self):
    response = self.client.get('/')
    self.assertEqual(response.context['theme'], 'home.css')
    self.assertEqual(response.context['active_page'], 'home')
    
  def test_home_sport_displayed(self):
    sport1 = Sport.objects.create(name='Football', description='Sport de ballon', image='/football.jpg')
    response = self.client.get('/')
  
    self.assertContains(response, sport1.name)
    
  def redirect_home_on_error_page(self, mock_sports):
    mock_sports.side_effect = Exception("Erreur de récupération des sports")
        
    response = self.client.get('/')
        
    self.assertEqual(response.status_code, 500)
        
    self.assertTemplateUsed(response, '404.html')
    self.assertContains(response, "Une erreur s'est produite")
    self.assertEqual(response.context['theme'], 'page_not_found.css')

class TestSportEventsView(TestCase):
  def test_sport_event_uses_correct_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')
    
  def test_home_context(self):
    response = self.client.get('/')
    self.assertEqual(response.context['theme'], 'home.css')
    self.assertEqual(response.context['active_page'], 'home')
    
  def test_home_sport_displayed(self):
    sport1 = Sport.objects.create(name='Football', description='Sport de ballon', image='/football.jpg')
    response = self.client.get('/')
  
    self.assertContains(response, sport1.name)
    
  def redirect_home_on_error_page(self, mock_sports):
    mock_sports.side_effect = Exception("Erreur de récupération des sports")
        
    response = self.client.get('/')
        
    self.assertEqual(response.status_code, 500)
        
    self.assertTemplateUsed(response, '404.html')
    self.assertContains(response, "Une erreur s'est produite")
    self.assertEqual(response.context['theme'], 'page_not_found.css')
  
  def setup(self):
    self.sport = Sport.objects.create(name="Basket", description="Un sport avec un ballon orange", image="/basket.jpg")
    self.stadium = Stadium.objects.create(name="Stade Basket", address="123 Rue du Basket", available_space=500)
    self.nation1 = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
    self.player1 = Player.objects.create(first_name="Michael", last_name="Jordan", nation=self.nation1, image="/michael_jordan.jpg")
    self.event = Event.objects.create(date="2025-06-01", time="20:00:00", sport=self.sport, stadium=self.stadium)
    self.event.player.add(self.player1)
    self.event.nation.add(self.nation1)
    
  def test_player_without_image(self):
    nation = self.nation1
    player = Player.objects.create(first_name="Wayne", last_name="Rooney", nation=nation, birth_date='1980-02-05')
    response = self.client.get(reverse('sport_events', args=['Hockey']))

    self.assertEqual(response.status_code, 200)

    json_data = response.json()
    event_data = json_data['events'][0]

    self.assertIsNone(event_data['players'][0].get('image_url'))

def test_nation_without_image(self):
    nation = Nation.objects.create(name="Canada", nickname="Canadiens")
    
    sport = Sport.objects.create(name="Hockey", description="Hockey sur glace")
    stadium = Stadium.objects.create(name="Stade Hockey", address="Adresse du stade", available_space=500)
    event = Event.objects.create(date="2025-06-01", time="20:00:00", sport=sport, stadium=stadium)
    event.nation.add(nation)

    response = self.client.get(reverse('sport_events', args=['Hockey']))
    self.assertEqual(response.status_code, 200)

    json_data = response.json()
    event_data = json_data['events'][0]

    self.assertIsNone(event_data['nations'][0].get('image_url'))
    
    
