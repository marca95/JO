from django.shortcuts import render

def ticket_view(request):
  theme = 'ticket.css'
  context = {
    'theme' : theme,
    'active_page' : 'ticket',
  }
  return render(request, 'ticket.html', context)
