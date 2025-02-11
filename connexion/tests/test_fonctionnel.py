from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class TestTicketFonctionnel(TestCase):
  
  def test_login_with_user_exists(self):
    self.user = User.objects.create_user(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    self.client.login(username='Toto', password='JesuislesacreJeanhub1!')
    
    response = self.client.get(reverse('panier'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'panier.html')
    
  def test_login_user_with_bad_password(self):
    self.user = User.objects.create_user(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    self.client.login(username='Toto', password='JesuisleJeanhub1!')
    
    response = self.client.get(reverse('login'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'connexion.html')
    
  def test_login_user_with_bad_username(self):
    self.user = User.objects.create_user(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    self.client.login(username='Toty', password='JesuislesacreJeanhub1!')
    
    response = self.client.get(reverse('login'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'connexion.html')
  
  def test_create_user_via_form(self):
    form_data = {
      'first_name': 'Jean-Hub',
      'last_name': 'Bert',
      'username': 'Toto',
      'email': 'IamJean-hub@bert.be',
      'password1': 'JesuislesacreJeanhub1!',
      'password2': 'JesuislesacreJeanhub1!',
      'accept_rgpd': True,
      'is_staff' : 0,
      'is_superuser': 0
    }

    response = self.client.post(reverse('signup'), form_data)

    user = User.objects.get(email='IamJean-hub@bert.be')
    
    self.assertEqual(user.first_name, 'Jean-Hub')
    self.assertEqual(user.last_name, 'Bert')
    self.assertEqual(user.username, 'Toto')
    self.assertEqual(user.email, 'IamJean-hub@bert.be')
    self.assertTrue(user.check_password('JesuislesacreJeanhub1!'))
    
  def test_create_user_with_similaire_data_via_form(self):
    User.objects.create(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    
    form_data = {
     'first_name': 'Harry',
     'last_name': 'Butter',
     'username': 'Toto',
     'email': 'IamJean-hub@bert.be',  
     'password1': 'JesuislesacreJeanhub1!',
     'password2': 'JesuislesacreJeanhub1!',
     'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
    self.assertFormError(response, 'form', 'email', 'Cet email est déjà utilisé.')
    
  def test_create_user_with_password_mismatch(self):
    form_data = {
      'first_name': 'Harry',
      'last_name': 'Butter',
      'username': 'Toto',
      'email': 'IamJean-hub@bert.be',  
      'password1': 'JesuislesacreJeanhub1!',
      'password2': 'JesuisJeanhub1!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'password2', 'Les mots de passe ne correspondent pas.')
    
  def test_create_user_with_password_fewer_characters(self):
    form_data = {
      'first_name': 'Harry',
      'last_name': 'Butter',
      'username': 'Toto',
      'email': 'IamJean-hub@bert.be',  
      'password1': 'JesuislesacreJeanhub!',
      'password2': 'JesuislesacreJeanhub!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertEqual(response.status_code, 302)
    
  def test_create_user_with_name_too_short(self):
    form_data = {
      'first_name': 'H',
      'last_name': 'B',
      'username': 'Toto',
      'email': 'IamJean-hub@bert.be',  
      'password1': 'JesuislesacreJeanhub!',
      'password2': 'JesuislesacreJeanhub!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'first_name', 'Le champ Prénom est trop petit.')
    self.assertFormError(response, 'form', 'last_name', 'Le champ Nom est trop petit.')
    
  def test_create_user_with_data_too_long(self):
    form_data = {
      'first_name': 'H'*260,
      'last_name': 'B'*260,
      'username': 'T'*260,
      'email': 'IamJean-hub'*260+'@bert.be',  
      'password1': 'JesuislesacreJeanhub!',
      'password2': 'JesuislesacreJeanhub!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'first_name', 'Ensure this value has at most 150 characters (it has 260).')
    self.assertFormError(response, 'form', 'last_name', 'Ensure this value has at most 150 characters (it has 260).')
    self.assertFormError(response, 'form', 'username', 'Ensure this value has at most 150 characters (it has 260).')
    
  def test_create_user_with_special_characters(self):
    form_data = {
      'first_name': '<Jean-Hub>',
      'last_name': '<Bert>',
      'username': '<Toto>',
      'email': 'IamJean-hub@bert.be',
      'password1': 'JesuislesacreJeanhub1!',
      'password2': 'JesuislesacreJeanhub1!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'first_name', 'Le champ Prénom ne peut pas contenir de caractères spéciaux.')
    self.assertFormError(response, 'form', 'last_name', 'Le champ Nom ne peut pas contenir de caractères spéciaux.')
    self.assertFormError(response, 'form', 'username', 'Le champ Nom d\'utilisateur ne peut pas contenir de caractères spéciaux.')
    
  def test_create_user_without_accept_rgpd(self):
    form_data = {
     'first_name': 'Harry',
     'last_name': 'Butter',
     'username': 'Toto',
     'email': 'IamJean-hub@bert.be',  
     'password1': 'JesuislesacreJeanhub1!',
     'password2': 'JesuislesacreJeanhub1!',
     'accept_rgpd': False,
    }    
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'accept_rgpd', 'Vous devez accepter les conditions RGPD pour vous inscrire.')
    
  def test_create_user_without_number(self):
    form_data = {
      'first_name': 'Harry',
      'last_name': 'Butter',
      'username': 'Toto',
      'email': 'IamJean-hub@bert.be',  
      'password1': 'Jehub1!',
      'password2': 'Jehub1!',
      'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')
    
  def test_update_user_without_data(self):
    User.objects.create(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    
    form_data = {
     'first_name': '',
     'last_name': '',
     'username': '',
     'email': 'IamJean-hub@bert.be',  
     'password1': 'JesuislesacreJeanhub1!',
     'password2': 'JesuislesacreJeanhub1!',
     'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'first_name', 'This field is required.')
    self.assertFormError(response, 'form', 'last_name', 'This field is required.')  
    self.assertFormError(response, 'form', 'username', 'This field is required.')    
    
  def test_update_data_with_email_invalid(self):
    User.objects.create(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    
    form_data = {
     'first_name': 'Harry',
     'last_name': 'Butter',
     'username': 'Toto',
     'email': 'IamJean-hubbert.be',  
     'password1': 'JesuislesacreJeanhub1!',
     'password2': 'JesuislesacreJeanhub1!',
     'accept_rgpd': True,
    }
    
    response = self.client.post(reverse('signup'), form_data)
    self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')  
    
  def test_update_data_with_form(self):
    self.user = User.objects.create_user(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    self.client.login(username='Toto', password='JesuislesacreJeanhub1!')
    
    update_user = {
      'update' : 1,
      'first_name': 'Joseph',
      'last_name': 'Albert',
      'email': 'jo@albert.gr',
      'username': 'Iamthebeber',
    }
    
    response = self.client.post(reverse('personal_data'), update_user)
    
    self.user.refresh_from_db()
    
    self.assertEqual(self.user.first_name, 'Joseph')
    self.assertEqual(self.user.last_name, 'Albert')
    self.assertEqual(self.user.username, 'Iamthebeber')
    self.assertEqual(self.user.email, 'jo@albert.gr')
    
  def test_update_user_with_same_data_other_user_with_form(self):
    User.objects.create_user(
      username='Toto',
      first_name='Jean-Hub',
      last_name='Bert',
      email='IamJean-hub@bert.be',
      password='JesuislesacreJeanhub1!',
    )
    
    self.user = User.objects.create_user(
      username='Victor',
      first_name='Victor',
      last_name='Vincent',
      email='victorviencent@bert.be',
      password='Jesuislevincent1!',
    )
        
    self.client.login(username='Victor', password='Jesuislevincent1!')
    
    update_user = {
      'update' : 1,
      'username': 'Toto',
      'first_name': self.user.first_name,
      'last_name': self.user.last_name,
      'email':'IamJean-hub@bert.be',
    }
    
    response = self.client.post(reverse('personal_data'), update_user)
    
    self.user.refresh_from_db()
    
    self.assertEqual(self.user.username, 'Victor')
    self.assertEqual(self.user.first_name, 'Victor')
    self.assertEqual(self.user.last_name, 'Vincent')
    self.assertEqual(self.user.email, 'victorviencent@bert.be')
    
  def test_remove_account_with_form(self):
   
    self.user = User.objects.create_user(
      username='Victor',
      first_name='Victor',
      last_name='Vincent',
      email='victorviencent@bert.be',
      password='Jesuislevincent1!',
    )
        
    self.client.login(username='Victor', password='Jesuislevincent1!') 
    
    delete_user = {'delete' : 1}
    
    response = self.client.post(reverse('personal_data'), delete_user)
    
    self.assertFalse(User.objects.filter(id=self.user.id).exists())
