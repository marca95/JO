from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UpdateFormSignupUser, UpdateFormLoginUser, CustomSetPasswordForm
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import pyotp

def connexion(request, action):
    theme = 'connexion.css'

    if action == 'login': 
        if request.method == 'POST':
            form = UpdateFormLoginUser(request, data=request.POST) 
            if form.is_valid():
                user = form.get_user()

                request.session["otp_user_id"] = user.id  

                otp_secret = pyotp.random_base32()
                otp_code = pyotp.TOTP(otp_secret).now()

                request.session["otp_secret"] = otp_secret  
                request.session.set_expiry(300)  

                send_mail(
                    "Votre code OTP",
                    f"Votre code OTP est : {otp_code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],  
                    fail_silently=False,
                )

                messages.info(request, "Un code OTP vous a été envoyé par e-mail.")
                return redirect('otp_verification')  

            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")

        else:
            form = UpdateFormLoginUser()

    elif action == 'signup':
        if request.method == 'POST':
            form = UpdateFormSignupUser(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre compte a été créé avec succès.")
                return redirect('login')
            else:
                messages.error(request, "Une erreur est survenue lors de l'enregistrement")
        else:
            form = UpdateFormSignupUser()
      
    context = {
        'theme': theme,
        'active_page': 'connexion',
        'form': form,
        'action': action
    }

    return render(request, 'connexion.html', context)

def otp_verification(request):
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        otp_secret = request.session.get("otp_secret")

        if otp_secret:
            totp = pyotp.TOTP(otp_secret)
            expected_otp = totp.now()
            print(f'OTP attendu (serveur) : {expected_otp}')

            if totp.verify(otp_code, valid_window=1): 
                user_id = request.session.get("otp_user_id")
                user = User.objects.get(id=user_id)

                login(request, user)  
                del request.session["otp_user_id"] 
                del request.session["otp_secret"]

                messages.success(request, "Connexion réussie avec OTP.")
                return redirect("panier")  

        messages.error(request, "Code OTP invalide ou expiré")
    
    return render(request, "verification.html", {'theme' : 'connexion.css'})


class CustomPasswordResetDoneView(PasswordResetDoneView) :
  template_name = 'password_reset_done.html'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
      context['theme'] = 'connexion.css'
      
      return context
    
class CustomPasswordResetView(PasswordResetView) :
  template_name = 'password_reset.html'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
      context['theme'] = 'connexion.css'
      
      return context
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView) :
  template_name = 'password_reset_confirm.html'
  form_class = CustomSetPasswordForm
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
      context['theme'] = 'connexion.css'
      
      return context
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView) :
  template_name = 'password_reset_complete.html'
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      
      context['theme'] = 'connexion.css'
      
      return context
