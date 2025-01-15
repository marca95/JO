from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User

class UpdateFormSignupUser(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Prénom")
    last_name = forms.CharField(max_length=150, required=True, label="Nom")
    email = forms.EmailField(max_length=255, required=True, label="Adresse email")
    username = forms.CharField(max_length=150, required=True, label="Nom d'utilisateur")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Mot de passe",
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email
      
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False       
        user.is_superuser = False  
        if commit:
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
        help_text=('Votre mot de passe doit contenir au moins 8 caractères et inclure des chiffres et des lettres.')
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
        return password1