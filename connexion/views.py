from django.shortcuts import render

def connexion(request):
  theme = 'connexion.css'
  context = {
    'theme' : theme,
    'active_page' : 'connexion',
  }
  return render(request, 'connexion.html', context)
