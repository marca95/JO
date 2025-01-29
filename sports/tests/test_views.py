from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from sports.models import *

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

    @patch('sports.views.Sport.objects.all')
    def test_redirect_home_on_error_page(self, mock_sports):
        mock_sports.side_effect = Exception("Erreur de récupération des sports")
        response = self.client.get('/fd')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.context['theme'], 'page_not_found.css')

class TestSportEventsView(TestCase):
    def setUp(self):
        self.sport = Sport.objects.create(name="Basket", description="Un sport avec un ballon orange", image="/basket.jpg")
        self.stadium = Stadium.objects.create(name="Stade Basket", address="123 Rue du Basket", available_space=500)
        self.nation1 = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
        self.player1 = Player.objects.create(first_name="Michael", last_name="Jordan", nation=self.nation1, image="/michael_jordan.jpg", birth_date='1980-02-05')
        self.event = Event.objects.create(date="2025-06-01", hour="20:00:00", sport=self.sport, stadium=self.stadium)
        self.event.player.add(self.player1)
        self.event.nation.add(self.nation1)

    def test_player_without_image(self):
        player = Player.objects.create(first_name="Wayne", last_name="Rooney", nation=self.nation1, birth_date='1980-02-05')
        self.event.player.add(player)

        response = self.client.get(reverse('sport_events', args=['Basket']))
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        event_data = json_data['events'][0]
        self.assertEqual(event_data['players'][1].get('image_url'), '/players/default_image.jpg')

    def test_nation_without_image(self):
        nation = Nation.objects.create(name="Canada", nickname="Canadiens")
        self.event.nation.add(nation)

        response = self.client.get(reverse('sport_events', args=['Basket']))
        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        event_data = json_data['events'][0]
        self.assertIsNone(event_data['nations'][1].get('image_url'))
