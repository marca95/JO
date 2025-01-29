from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ticket.models import Ticket
from sports.models import Stadium, Nation, Event, Sport
from panier.models import Cart
from datetime import date, time
  
class TestPanierViews(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(first_name="test", last_name="user", email="test@user.tr", username="testuser", password="password123")
    self.sport = Sport.objects.create(name="Basketball", description="Un sport")
    self.stadium = Stadium.objects.create(name="Stade de basket", address="123 Rue du sport", available_space=1000)
    self.nation = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
    self.event = Event.objects.create(
            date=date(2025,12,23),
            hour=time(20,0),
            sport=self.sport,
            stadium=self.stadium,
        )
    self.ticket = Ticket.objects.create(nbr_place=1, price=10, formula='test', event=self.event)
    self.ticket2 = Ticket.objects.create(nbr_place=2, price=20, formula='test2', event=self.event)

  def test_panier_view(self):
    self.client.login(username='testuser', password='password123')
    response = self.client.get(reverse('panier') + '?ticket_id=' + str(self.ticket.id))
    self.assertIn('events', response.context) 
    
  def test_panier_view_with_ticket(self):
    self.client.login(username='testuser', password='password123')
    response = self.client.get(reverse('panier') + f'?ticket_id={self.ticket.id}')
        
    events = response.context['events']
    self.assertEqual(len(events), 1)
    event_data = events[0]

    formatted_date = self.event.date.strftime('%d/%m/%Y')
    self.assertEqual(event_data['date'], formatted_date)
    formatted_hour = self.event.hour.strftime('%Hh%M')
    self.assertEqual(event_data['hour'], formatted_hour)
    self.assertEqual(event_data['ticket_id'], self.ticket.id)
    self.assertEqual(event_data['stadium_name'], self.stadium.name)
    self.assertEqual(event_data['sport_name'], self.sport.name)
    self.assertEqual(event_data['ticket_price'], self.ticket.price)
    self.assertEqual(event_data['nbr_places'], self.ticket.nbr_place)
    self.assertEqual(event_data['formula'], self.ticket.formula)
    
    self.assertTrue(response.context['is_authenticated'])
    
  def test_create_cart_if_not_exists(self):
    self.client.login(username='testuser', password='password123')

    ticket_ids = [self.ticket.id, self.ticket2.id]
    response = self.client.post(reverse('panier_check'), {'ticket_ids': ticket_ids})

    cart = Cart.objects.get(user=self.user)
    self.assertIsNotNone(cart)  
    self.assertIsNotNone(cart.first_key)
    self.assertNotEqual(cart.first_key, '')  

    self.assertEqual(cart.tickets.count(), 2)
    self.assertIn(self.ticket, cart.tickets.all())
    self.assertIn(self.ticket2, cart.tickets.all())

  def test_no_duplicate_cart_for_user(self):
    self.client.login(username='testuser', password='password123')

    Cart.objects.create(user=self.user)
    cart = Cart.objects.get(user=self.user)
    self.assertIsNotNone(cart)  
    self.assertEqual(Cart.objects.filter(user=self.user).count(), 1)  
    self.assertIsNotNone(cart.first_key)

    
    
