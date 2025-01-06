from django.shortcuts import render

def home(request):
  theme = 'home.css'
  context = {
    'theme' : theme,
    'active_page' : 'home',
  }
  return render(request, 'home.html', context)
