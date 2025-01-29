from django.test import TestCase
from panier.forms import PersonalDataForm

class TestPersonalDataForm(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'testuser',
            'first_name': 'Jacky',
            'last_name': 'Tuning',
            'email': 'Jacky.Tuning@vr.com',
        }
        form = PersonalDataForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())
        
    def test_invalid_username_empty(self):
        data = {
            'username': '',
            'first_name': 'Jacky',
            'last_name': 'Tuning',
            'email': 'Jacky.Tuning@vr.com',
        }
        form = PersonalDataForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This field is required.'])

    def test_invalid_username_special_characters(self):
        data = {
            'username': 'user><#',
            'first_name': 'Jacky',
            'last_name': 'Tuning',
            'email': 'Jacky.Tuning@vr.com',
        }
        form = PersonalDataForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Le champ Nom utilisateur ne peut pas contenir de caractères spéciaux.'])

    def test_invalid_first_name_too_short(self):
        data = {
            'username': 'testuser',
            'first_name': 'J',
            'last_name': 'Tuning',
            'email': 'Jacky.Tuning@vr.com',
        }
        form = PersonalDataForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'], ['Le champ Prénom est trop petit.'])

    def test_invalid_email_empty(self):
        data = {
            'username': 'testuser',
            'first_name': 'Jacky',
            'last_name': 'Tuning',
            'email': '',
        }
        form = PersonalDataForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_invalid_email_special_characters(self):
        data = {
            'username': 'testuser',
            'first_name': 'Jacky',
            'last_name': 'Tuning',
            'email': 'Jacky.Tuning@ex#ample.com',
        }
        form = PersonalDataForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
