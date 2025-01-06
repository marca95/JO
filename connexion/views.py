from django.shortcuts import render

def connexion(request):
  return render(request, 'connexion.html', {'active_page' : 'connexion'})
