from django.shortcuts import render, redirect
from ticket.models import Ticket
from panier.models import Cart
from django.contrib.auth.decorators import login_required
import uuid

def panier(request):
    theme = 'panier.css'

    ticket_ids = request.GET.getlist("ticket_id")  

    events = []

    if ticket_ids:
        tickets = Ticket.objects.filter(id__in=ticket_ids).select_related('event')

        for ticket in tickets:
            event = ticket.event
            formatted_date = event.date.strftime('%d/%m/%Y')
            hour = event.hour.strftime('%Hh%M')
            event_data = {
                "ticket_id": ticket.id,
                "date": formatted_date,
                "hour": hour,
                "stadium_name": event.stadium.name,
                "sport_name": event.sport.name,
                "ticket_price": ticket.price,
                "nbr_places": ticket.nbr_place,
                "formula": ticket.formula
            }
            events.append(event_data)

    context = {
        'theme': theme,
        'events': events,
        'is_authenticated': request.user.is_authenticated,
    }

    return render(request, 'panier.html', context)

def generate_key():
    return str(uuid.uuid4())

def panier_check(request): 
    if request.method == "POST":
        ticket_ids = request.POST.getlist('ticket_ids')  # Récupération des IDs des tickets
        tickets = Ticket.objects.filter(id__in=ticket_ids)  # Filtrage des tickets
        cart, created = Cart.objects.get_or_create(user=request.user)  # Récupérer ou créer le panier

        if not cart.first_key:
            cart.first_key = generate_key()  
            cart.save()

        cart.second_key = generate_key()  
        cart.save()

        ticket_qr_code = cart.first_key + cart.second_key

        for ticket in tickets:
            ticket.cart = cart
            ticket.qr_code = ticket_qr_code  
            ticket.save()

        return redirect('payment')  
    else: 
        return redirect('panier')