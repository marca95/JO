from django.test import TestCase
from django.contrib.auth.models import User
from connexion.forms import UpdateFormSignupUser, UpdateFormLoginUser, UpdateFormForgotPassword, CustomSetPasswordForm

class TestConnexionForms(TestCase):
  def test_signup_form_valid(self):
    form_data = {
      'first_name': 'Victor',
      'last_name': 'Vincent',
      'email': 'Victor.Vincent@example.com',
      'username': 'vvincent',
      'password1': 'Magie01?',
      'password2': 'Magie01?',
      'accept_rgpd': True
    }
    form = UpdateFormSignupUser(data=form_data)
    self.assertTrue(form.is_valid())  

  def test_signup_form_invalid_email(self):
    form_data = {
      'first_name': 'Victor',
      'last_name': 'Vicent',
      'email': 'victor.vincent@mental.com',
      'username': 'vvincent',
      'password': 'Magie01?',
      }
    User.objects.create_user(**form_data)  

    form_data['email'] = 'victor.vincentmental.com'
    form = UpdateFormSignupUser(data=form_data)
    self.assertFalse(form.is_valid()) 
    self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

  def test_signup_form_password_mismatch(self):
    form_data = {
      'first_name': 'Victor',
      'last_name': 'Vincent',
      'email': 'Victor.Vincent@example.com',
      'username': 'vvincent',
      'password1': 'Magie01?',
      'password2': 'Magie02?',
      'accept_rgpd': True
    }
    form = UpdateFormSignupUser(data=form_data)
    self.assertFalse(form.is_valid())  
    self.assertEqual(form.errors['password2'], ['Les mots de passe ne correspondent pas.'])

  def test_signup_form_missing_required_fields(self):
    form_data = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'username': '',
        'password1': '',
        'password2': '',
        'accept_rgpd': False
    }
    form = UpdateFormSignupUser(data=form_data)
    self.assertFalse(form.is_valid())  

  def test_login_form_valid(self):
    user = User.objects.create_user(username='vvincent', password='Magie01?')
    form_data = {'username': 'vvincent', 'password': 'Magie01?'}
    form = UpdateFormLoginUser(data=form_data)
    self.assertTrue(form.is_valid())  

  def test_login_form_invalid_username(self):
    form_data = {'username': 'vincen', 'password': 'Magie01?'}
    form = UpdateFormLoginUser(data=form_data)
    self.assertFalse(form.is_valid()) 

  def test_login_form_invalid_password(self):
    user = User.objects.create_user(username='vvincent', password='Magie02?')
    form_data = {'username': 'vvincent', 'password': 'Magie01?'}
    form = UpdateFormLoginUser(data=form_data)
    self.assertFalse(form.is_valid())  

  def test_forgot_password_form_valid(self):
    form_data = {'email': 'Victor.Vincent@example.com'}
    form = UpdateFormForgotPassword(data=form_data)
    self.assertTrue(form.is_valid())  

  def test_forgot_password_form_invalid_email(self):
    form_data = {'email': 'Victorincentexample.com'}
    form = UpdateFormForgotPassword(data=form_data)
    self.assertFalse(form.is_valid())  

  def test_set_password_form_valid(self):
    form_data = {
      'new_password1': 'Magie55?!',
      'new_password2': 'Magie55?!'
      }
    form = CustomSetPasswordForm(user=User.objects.create_user(username='vvincent', password='Magie55?!'), data=form_data)
    self.assertTrue(form.is_valid()) 

  def test_set_password_form_invalid_password_mismatch(self):
    form_data = {
      'new_password1': 'Magie66?!!',
      'new_password2': 'Magie77?!'
     }
    form = CustomSetPasswordForm(user=User.objects.create_user(username='vvincent', password='Magie55?!'), data=form_data)
    self.assertFalse(form.is_valid())  

  def test_set_password_form_invalid_special_characters(self):
    form_data = {
        'new_password1': 'Magie55?!<script>',
        'new_password2': 'Magie55?!<script>'
      }
    form = CustomSetPasswordForm(user=User.objects.create_user(username='vvincent', password='Magie55?!<script>'), data=form_data)
    self.assertFalse(form.is_valid()) 
