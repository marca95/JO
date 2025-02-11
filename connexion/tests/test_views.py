from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ConnexionViewTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='Jean', password='Traineau1?')
        
  def test_login_post_success(self):
    response = self.client.post(reverse('login'), {
      'username': 'Jean',
      'password': 'Traineau1?',
    }, follow=True)
        
    self.assertRedirects(response, reverse('otp_verification'))
    self.assertFalse('_auth_user_id' in self.client.session)
      
  def test_login_wrong_password(self):
    response = self.client.post(reverse('login'), {
      'username': 'Jean',
      'password': 'AiMar',
    })

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'connexion.html')  
    
  def test_login_wrong_username(self):
    response = self.client.post(reverse('login'), {
      'username': 'Robert',
      'password': 'Traineau1?',
    })

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'connexion.html')  
    
  def test_signup_post_success(self):
    response = self.client.post(reverse('signup'), {
    'username': 'Vivi',
    'last_name': 'Victoria',
    'first_name': 'Beckman',
    'password1': 'Jesuislavivi1!',
    'password2': 'Jesuislavivi1!',
    'email': 'vividjacket1@tbr.com',
    'accept_rgpd': True,
    }, follow=True)

    self.assertEqual(response.status_code, 200)
    self.assertRedirects(response, reverse('login'))  
    self.assertTrue(User.objects.filter(username='Vivi').exists())  
    
  def test_signup_post_fail(self):
    response = self.client.post(reverse('signup'), {
      'username': 'Vivi',
      'password1': 'Jesuislavivi1!',
      'password2': 'Gmesuistrompe1!',
      'email': 'vividjacket1@tbr.com',
      'last_name': 'Victoria',
      'first_name': 'Beckman',
      'accept_rgpd': True,
    }, follow=False)

    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'connexion.html')
    self.assertFalse(User.objects.filter(username='Vivi').exists()) 



 