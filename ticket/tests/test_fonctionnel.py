from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ticket.models import Ticket
from sports.models import *

class AdminTicketCRUDTest(TestCase):
  def setUp(self):
    self.admin = User.objects.create_superuser(
      username='Henry', 
      first_name='Henry', 
      last_name='Salvator', 
      password='Jesuishenry1?', 
      is_superuser = True, 
      is_staff = True,
      email='henryS@yahoo.tv'
    )
    self.client.login(username='Henry', password='Jesuishenry1?')
    
    self.sport = Sport.objects.create(name="Basketball", description="Un sport")
    self.stadium = Stadium.objects.create(name="Stade de basket", address="123 Rue du sport", available_space=1000)
    self.nation = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
    self.event = Event.objects.create(date='2025-02-11', hour='11:30', admin=self.admin, sport=self.sport, stadium=self.stadium)
    self.ticket = Ticket.objects.create(price=11, formula='test', event=self.event, nbr_place=2)
  
  def test_admin_view_on_ticket(self):
    url = reverse("admin:ticket_ticket_changelist")
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    
  def test_admin_add_ticket(self):
    url = reverse("admin:ticket_ticket_add")
    ticket2 = {
      'price':'22', 
      'formula':'test2', 
      'event':self.event.id, 
      'nbr_place':'3'
      }
    response = self.client.post(url, ticket2, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(Ticket.objects.filter(formula='test2').exists())
    
  def test_admin_update_ticket(self):
    url = reverse("admin:ticket_ticket_change", args=[self.ticket.id])
    ticket_updated = {
      'price':'15', 
      'formula':'test2',
      'event':self.event.id,
      'nbr_place':3
      }      
    
    response = self.client.post(url, ticket_updated, follow=True)
    
    self.assertEqual(response.status_code, 200)
    self.ticket.refresh_from_db()
    self.assertEqual(self.ticket.price, 15)
    self.assertEqual(self.ticket.formula, 'test2')
    self.assertEqual(self.ticket.nbr_place, 3)
    
  def test_admin_can_delete_ticket(self):
    url = reverse("admin:ticket_ticket_delete", args=[self.ticket.id])
    response = self.client.post(url, {"post": "yes"}, follow=True)
    self.assertEqual(response.status_code, 200)
    self.assertFalse(Ticket.objects.filter(id=self.ticket.id).exists())