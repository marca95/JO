from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import Http404
from .forms import UpdateFormSignupUser, UpdateFormLoginUser

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
    else :
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
    else : 
      form = UpdateFormSignupUser()
      
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
