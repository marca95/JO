from django.test import TestCase
from django.urls import reverse
from sports.models import Sport

class TicketViewTest(TestCase):
  def setUp(self):
    Sport.objects.create(name="Ping-pong", image="pingpong_image.jpg")
    Sport.objects.create(name="Waterpolo", image="waterpolo_image.jpg")
    
  def test_length_character_string(self):
    sport1 = Sport.objects.get(name="Ping-pong")
    sport2 = Sport.objects.get(name="Waterpolo")
    
    self.assertLessEqual(len(sport1.name), 50)
    self.assertLessEqual(len(sport2.name), 50)    
