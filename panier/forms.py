from django import forms
from django.core.exceptions import ValidationError
# from django.utils.html import escape
from django.contrib.auth.models import User

def validate_input(value, field_name):
    if value is None or not value.strip():
        raise ValidationError(f"Le champ {field_name} est obligatoire.")
    if any(char in value for char in "#$%^&*()[]{};:<>/\\|`~=_+"):
        raise ValidationError(f"Le champ {field_name} ne peut pas contenir de caractères spéciaux.")
    if len(value.strip()) < 3:
        raise ValidationError(f"Le champ {field_name} est trop petit.")
    if len(value.strip()) > 150:
        raise ValidationError(f"Le champ {field_name} est trop long.")
    return value

class PersonalDataForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Nom utilisateur")
    first_name = forms.CharField(max_length=150, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    email = forms.EmailField(max_length=255, required=True, label="Adresse email")
    
    def clean_username(self):
        username = self.cleaned_data.get('username')  
        if not username:  
            raise ValidationError("Le champ Nom utilisateur est obligatoire.")
        return validate_input(username, "Nom utilisateur")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return validate_input(first_name, "Prénom")
        return first_name  

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return validate_input(last_name, "Nom")
        return last_name 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return validate_input(email, "email")
        return email 

