from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from panier.models import Cart
from django.core.exceptions import ValidationError
import uuid

def generate_key():
    return str(uuid.uuid4())

def validate_input(value, field_name):
    if not value.strip(): 
        raise ValidationError(f"Le champ {field_name} est obligatoire.")
    if any(char in value for char in "#$%^&*()[]{};:<>/\\|`~=_+"): 
        raise ValidationError(f"Le champ {field_name} ne peut pas contenir de caractères spéciaux.")
    if len(value.strip()) < 3:  
        raise ValidationError(f"Le champ {field_name} est trop petit.")
    if len(value.strip()) > 150:  
        raise ValidationError(f"Le champ {field_name} est trop long.")
    return value
    
class UpdateFormSignupUser(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    email = forms.EmailField(max_length=255, required=True, label="Adresse email")
    username = forms.CharField(max_length=150, required=True, label="Nom d'utilisateur")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
        help_text=(
            'Votre mot de passe doit respecter les règles suivantes :'
            '<p class="safety_policy">- Contenir au moins 8 caractères.</p>'
            '<p class="safety_policy">- Contenir au moins un chiffre.</p>'
            '<p class="safety_policy">- Contenir au moins une lettre majuscule.</p>'
            '<p class="safety_policy">- Contenir au moins un caractère spécial (?!.@,).</p>'
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmez le mot de passe",
    )
    accept_rgpd = forms.BooleanField(
        required=True,
        label="J'accepte les conditions RGPD",
        error_messages={
            "required": "Vous devez accepter les conditions RGPD pour vous inscrire."
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password1', 
            'password2'
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return validate_input(first_name, "Prénom")
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return validate_input(last_name, "Nom")
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return validate_input(username, "Nom d'utilisateur")

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if password2 != self.cleaned_data.get('password1'):
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False       
        user.is_superuser = False  
        if commit:
            Cart.objects.create(
                user=user,
                first_key=generate_key()
            )
            
            user.save()
            
        return user


class UpdateFormLoginUser(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur") 
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
    )
    
class UpdateFormForgotPassword(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput,
        label="Adresse e-mail",
    )
    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=('Nouveau mot de passe'),
        widget=forms.PasswordInput(),
        help_text=(
            'Votre mot de passe doit respecter les règles suivantes :'
            '<p class="safety_policy">- Contenir au moins 8 caractères.</p>'
            '<p class="safety_policy">- Contenir au moins un chiffre.</p>'
            '<p class="safety_policy">- Contenir au moins une lettre majuscule.</p>'
            '<p class="safety_policy">- Contenir au moins un caractère spécial (?!.@,).</p>'
        )
    )

    new_password2 = forms.CharField(
        label=('Confirmer le mot de passe'),
        widget=forms.PasswordInput(),
        help_text=('Confirmez votre nouveau mot de passe en le retapant.')
    )

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if len(password1) < 8:
            raise forms.ValidationError(('Le mot de passe doit comporter au moins 8 caractères.'))
        
        if len(password1) > 150:
            raise forms.ValidationError(('Le mot de passe est trop long.'))
        
        special_characters = {'?', '!', '.', '@', ','}
        if not any(char in special_characters for char in password1):
            raise forms.ValidationError(('Le mot de passe doit comporter au moins un caractère spécial (?!.@,).'))
        
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError(('Le mot de passe doit comporter au moins un chiffre.'))
        
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError(('Le mot de passe doit comporter au moins une lettre majuscule.'))
        
        if any(char in "#$%^&*()[]{};:<>/\\|`~=_+" for char in password1): 
            raise ValidationError(('Le mot de passe contient un caractère non autorisé.'))
        
        return password1