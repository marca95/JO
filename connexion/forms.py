from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username