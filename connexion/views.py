from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.http import Http404
from .forms import UpdateFormSignupUser, UpdateFormLoginUser

def connexion(request, action):
  theme = 'connexion.css'
    
  if action == 'login' : 
    form = UpdateFormLoginUser(request.POST or None)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('home')
  elif action == 'signup' :
    form = UpdateFormSignupUser(request.POST or None)
    if form.is_valid():
      form.save()
      return redirect('login')
  elif action == 'password':
      return redirect('password_reset')
  else :
     raise Http404('Page pas trouvé')
      
  context = {
  'theme' : theme,
  'active_page' : 'connexion',
  'form' : form, 
  'action' : action
    }

  return render(request, 'connexion.html', context)
