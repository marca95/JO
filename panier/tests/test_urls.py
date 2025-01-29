from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ticket.models import Ticket
from sports.models import Stadium, Nation, Event, Sport
from panier.models import Cart

class TestPanierUrls(TestCase):
    
  def setUp(self):
    self.user = User.objects.create_user(first_name="test", last_name="user", email="test@user.tr", username="testuser", password="password123")
    self.sport = Sport.objects.create(name="Basketball", description="Un sport")
    self.stadium = Stadium.objects.create(name="Stade de basket", address="123 Rue du sport", available_space=1000)
    self.nation = Nation.objects.create(name="USA", nickname="Américains", image="/usa.jpg")
    self.event = Event.objects.create(
            date="2025-12-23",
            hour="20:00:00",
            sport=self.sport,
            stadium=self.stadium,
        )
    self.ticket = Ticket.objects.create(nbr_place=1, price=10, formula='test', event=self.event)
    self.cart = Cart.objects.create(user=self.user, first_key="abcd", second_key="efgh")

  def test_panier_url(self):
    response = self.client.get(reverse('panier'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'panier.html')

  def test_panier_check_url(self):
    self.client.login(username="testuser", password="password123")
    response = self.client.get(reverse('panier_check'))
    self.assertEqual(response.status_code, 302) 
    self.assertRedirects(response, reverse('state'))

  def test_status_url(self):
    response = self.client.get(reverse('state'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'payment_state.html')

  def test_personal_data_url(self):
    self.client.login(username="testuser", password="password123")
    response = self.client.get(reverse('personal_data'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'personal_data.html')

  def test_rgpd_url(self):
    response = self.client.get(reverse('rgpd'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'rgpd.html')

  def test_mentions_url(self):
      response = self.client.get(reverse('mentions'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'mentions_legales.html')

  def test_cgv_url(self):
      response = self.client.get(reverse('cgv'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'cgv.html')

  def test_cgu_url(self):
      response = self.client.get(reverse('cgu'))
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'cgu.html')
