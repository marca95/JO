from django.test import TestCase
from django.urls import reverse
from sports.models import Sport, Event, Stadium, Nation, Player
from ticket.models import Ticket


class TestTicketViews(TestCase):
  def setUp(self):
    self.sport = Sport.objects.create(name="Football", description="Sport dangereux", image="football.jpg")
    self.stadium = Stadium.objects.create(name="Stade de Football", address="123 Rue du Stade", available_space=500)
    self.nation = Nation.objects.create(name="France", nickname="Les Bleus", image="france.jpg")
    self.player = Player.objects.create(first_name="Jean", last_name="Gos", nation=self.nation, image="JeanGos.jpg", birth_date='1988-02-19')
    self.event = Event.objects.create(
        date="2025-04-19",
        hour="01:12:00",
        sport=self.sport,
        stadium=self.stadium
    )
    self.event.nation.add(self.nation)
    self.event.player.add(self.player)
    
    self.ticket_url = reverse('ticket')
    self.ticket_events_url = reverse('ticket_events', args=['Football'])
    self.ticket_detail_url = reverse('ticket_detail', args=['Football', self.event.id])
  
  def test_ticket_view_contains_expected_content(self):
    response = self.client.get(self.ticket_url)
    self.assertContains(response, 'Football')  
  
  def test_ticket_events_view_contains_expected_content(self):
    response = self.client.get(self.ticket_events_url)
    self.assertContains(response, 'Football')  
    self.assertContains(response, self.sport.name)  
  
  def test_ticket_view_template_used(self):
    response = self.client.get(self.ticket_url)
    self.assertTemplateUsed(response, 'ticket.html')
  
  def test_ticket_events_view_json(self):
    response = self.client.get(self.ticket_events_url)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response['Content-Type'], 'application/json')
  
  def test_ticket_detail_view_template_used(self):
    response = self.client.get(self.ticket_detail_url)
    self.assertTemplateUsed(response, 'detail.html')
