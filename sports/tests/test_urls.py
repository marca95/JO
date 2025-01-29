from django.test import TestCase
from django.urls import reverse, resolve
from sports.views import *

class TestUrls(TestCase):
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

    def test_sport_events_url_status_code_valid(self):
        valid_sports = ['Football', 'Basket']
        for sport_name in valid_sports: 
            response = self.client.get(reverse('sport_events', args=[sport_name]))
            self.assertEqual(response.status_code, 200)

    def test_sport_events_url_not_found(self):
        invalid_sport = 'Toto'  
        response = self.client.get(reverse('sport_events', args=[invalid_sport]))
        self.assertTemplateUsed(response, '404.html')
