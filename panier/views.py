from django.shortcuts import render
from django.http import JsonResponse
from ticket.models import Ticket


def panier(request):
  theme = 'panier.css'
   
  context = {
    'theme' : theme,
    }
  
  return render(request, 'panier.html', context)

  
