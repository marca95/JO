from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
from ticket.models import Ticket

def home(request):
    theme = 'home.css'
    sports = Sport.objects.all()
    context = {
        'theme': theme,
        'active_page': 'home',
        'sports': sports
    }
    return render(request, 'home.html', context)

def sport_events(request, sport_name):
    try:
        sport = get_object_or_404(Sport, name=sport_name)
        events = sport.event_set.all()  
        event_data = []
        for event in events:
            formatted_date = event.date.strftime('%d/%m/%Y')
            
            tickets = Ticket.objects.filter(event=event)
            occupied_seats = 0

            for ticket in tickets:
                linked_carts = ticket.carts.all()
                if linked_carts.exists():
                    occupied_seats += ticket.nbr_place * linked_carts.count()

            available_space = event.stadium.available_space - occupied_seats 
            
            event_data.append({
                'id' : event.id,
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
                } for player in event.player.all()],
            })

            sport_image_url = sport.image.url if sport.image else None
        return JsonResponse({'events': event_data, 'sport_image_url': sport_image_url, 'sport_name' : sport.name})
    except Exception as e:
        return render(request, '404.html', {
            'error_message': 'Une erreur s\'est produite', 
            'theme':'page_not_found.css'
            })

