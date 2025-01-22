from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UpdateFormSignupUser, UpdateFormLoginUser, CustomSetPasswordForm

# from django.http import Http404
# from django.core.mail import send_mail
# from jo.settings.local import EMAIL_HOST_USER

def generate_key():
    return str(uuid.uuid4())

def connexion(request, action):
    theme = 'connexion.css'

    if action == 'login': 
        if request.method == 'POST':
            form = UpdateFormLoginUser(request, data=request.POST) 
            if form.is_valid():  
                user = form.get_user()
                login(request, user)  
                messages.success(request, "Connexion réussie.")
                return redirect('home')  
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

from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView

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
    
def rgpd(request, action):
    theme = 'connexion.css'
    
    context = {
      'theme': theme,
      'active_page': 'connexion',
      'action': action
    }
    
    return render(request, 'rgpd.html', context)