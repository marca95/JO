from django.shortcuts import render

def panier(request):
  theme = 'panier.css'
  context = {
    'theme' : theme,
    'active_page' : 'panier',
  }
  return render(request, 'panier.html', context)