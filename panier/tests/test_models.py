from django.test import TestCase
from panier.models import Cart
from ticket.models import Ticket
from sports.models import Sport,Nation, Stadium, Event
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

class TestPanierModels(TestCase):
  def setUp(self):
    self.user = User.objects.create(username="toto", first_name="Henrico", last_name="Bernardo", email="henricob@toto.dr", password="P4SSW0RD")
    self.cart = Cart.objects.create(first_key="abcd", second_key="efgh", user=self.user)
    
    self.sport = Sport.objects.create(name="Basketball", description="Un sport")
    self.stadium = Stadium.objects.create(name="Stade de basket", address="123 Rue du sport", available_space=1000)
    self.nation = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
    self.event = Event.objects.create(
            date="2025-12-23",
            hour="20:00:00",
            sport=self.sport,
            stadium=self.stadium,
        )

    self.ticket1 = Ticket.objects.create(nbr_place=1, price=10, formula='test1', event=self.event)
    self.ticket2 = Ticket.objects.create(nbr_place=2, price=20, formula='test2', event=self.event)
    self.cart.tickets.add(self.ticket1, self.ticket2)
    
  def test_only_one_cart_by_person(self):
    with self.assertRaises(IntegrityError):
      Cart.objects.create(first_key="ijkl", second_key="mnop", user=self.user)
      
  def test_delete_user_cart_exists(self):
    self.user.delete()
    self.assertFalse(Cart.objects.filter(user=self.user).exists())
    
  def test_nbr_character_max(self):
    first_key_max = "a" * 256
    second_key_max = "b" * 256
    self.cart = Cart(first_key=first_key_max, second_key=second_key_max, user=self.user)
    with self.assertRaises(ValidationError):
      self.cart.full_clean() 
      self.cart.save()
      
  def test_few_tickets_in_one_cart(self):
    self.assertTrue(self.cart.tickets.filter(id=self.ticket1.id).exists()) 
    self.assertTrue(self.cart.tickets.filter(id=self.ticket2.id).exists())
    self.assertEqual(self.cart.tickets.count(), 2)

  def test_type_character_on_ticket(self):
    self.assertIsInstance(self.cart.first_key, str)
    self.assertIsInstance(self.cart.second_key, str)
  
