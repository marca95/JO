from django.shortcuts import render

def ticket_view(request):
  return render(request, 'ticket.html', {'active_page' : 'ticket'})
