from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *

def home(request):
    theme = 'home.css'
    sports = Sport.objects.all()
    context = {
        'theme': theme,
        'active_page': 'home',
        'sports': sports
    }
    return render(request, 'home.html', context)

def sport_events(request, sport_id):
    try:
        sport = get_object_or_404(Sport, id=sport_id)
        events = sport.event_set.all()

        event_data = []
        for event in events:
            formatted_date = event.date.strftime('%d/%m/%Y')
            event_data.append({
                'date': formatted_date,
                'hour': event.hour.strftime('%H:%M'),
                'stadium': {
                    'name': event.stadium.name,
                    'address': event.stadium.address,
                    'available_space': event.stadium.available_space
                },
                'nations': [{
                    'name': nation.name,
                    'nickname': nation.nickname,
                    'image_url': nation.image.url if nation.image else None
                } for nation in event.nation.all()], # Je fais ca car j'ai une relation many to many
                'players': [{
                    'first_name': player.first_name,
                    'last_name': player.last_name,
                    'image_url': player.image.url if player.image else None
                } for player in event.players.all()], 
            })
            sport_image_url = sport.image.url if sport.image else None
            
        return JsonResponse({'events': event_data, 'sport_image_url': sport_image_url})
      
    except Exception as e:
        return JsonResponse({'error': 'Une erreur s\'est produite'}, status=500)

