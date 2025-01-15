from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from sports.models import *
from ticket.models import Ticket

def ticket_view(request):
  theme = 'ticket.css'
  sports = Sport.objects.all()
  context = {
    'theme' : theme,
    'active_page' : 'ticket',
    'sports': sports
  }
  return render(request, 'ticket.html', context)


def offre_view(request, sport_id):
    try:
        sport = get_object_or_404(Sport, id=sport_id)
        events = sport.event_set.all()  
        event_data = []

        for event in events:
            formatted_date = event.date.strftime('%d/%m/%Y')
            
            tickets = Ticket.objects.filter(event=event)
            occupied_seats = 0

            # Attention ce n'est pas vraiment juste, il faut valider le paiement pour diminuer le nombre de places

            for ticket in tickets:
                if ticket.formula == 'solo':
                    occupied_seats += 1
                elif ticket.formula == 'duo':
                    occupied_seats += 2
                elif ticket.formula == 'familiale':
                    occupied_seats += 4

            available_space = event.stadium.available_space - occupied_seats

            event_data.append({
                'id': event.id,
                'date': formatted_date,
                'hour': event.hour.strftime('%H:%M'),
                'stadium': {
                    'name': event.stadium.name,
                    'address': event.stadium.address,
                    'available_space': available_space if available_space >= 0 else 0,  
                },
                'nations': [{
                    'name': nation.name,
                    'nickname': nation.nickname,
                    'image_url': nation.image.url if nation.image else None
                } for nation in event.nation.all()],
                'players': [{
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'image_url': player.image.url if player.image else None
                } for player in event.players.all()],
                'tickets':[
                  {
                    "price": str(ticket.price), 
                    "formula": ticket.formula,
                  }
                  for ticket in event.tickets.all()
                ]
            })
            
            sport_image_url = sport.image.url if sport.image else None

        return JsonResponse({'events': event_data, 'sport_image_url': sport_image_url})

    except Exception as e:
        return JsonResponse({'error': 'Une erreur s\'est produite'}, status=500)

def detail_event(request, sport_id, event_id):
    try:
        sport = get_object_or_404(Sport, id=sport_id)
        event = get_object_or_404(Event, id=event_id, sport=sport)

        tickets = Ticket.objects.filter(event=event)
        occupied_seats = sum(
            (1 if ticket.formula == 'solo' else 2 if ticket.formula == 'duo' else 4)
            for ticket in tickets
        )
        available_space = event.stadium.available_space - occupied_seats

        event_data = {
            'id': event.id,
            'date': event.date.strftime('%d/%m/%Y'),
            'hour': event.hour.strftime('%H:%M'),
            'stadium': {
                'name': event.stadium.name,
                'address': event.stadium.address,
                'available_space': max(available_space, 0),
            },
            'nations': [{
                'name': nation.name,
                'image_url': nation.image.url if nation.image else None,
            } for nation in event.nation.all()],
            'tickets': [{
                'formula': ticket.formula,
                'price': str(ticket.price),
            } for ticket in tickets]
        }

        return JsonResponse({'event': event_data})
    except Exception as e:
        return JsonResponse({'error': 'Une erreur est survenue'}, status=500)
