from django.shortcuts import render, redirect
from django.contrib import messages
from ticket.models import Ticket
from panier.models import Cart
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from django.db import transaction
from django.core.exceptions import ValidationError
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm 
from django.utils.html import escape
from django.contrib.auth.models import User
from .forms import PersonalDataForm
from reportlab.lib.utils import ImageReader
from io import BytesIO
import qrcode
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
    }

    if request.user.is_authenticated:
        context['is_authenticated'] = True
        
    return render(request, 'panier.html', context)

def generate_key():
    return str(uuid.uuid4())

def panier_check(request): 
    theme = 'panier.css'
    context = {
        'theme' : theme }
        
    if request.method == "POST":
        ticket_ids = request.POST.getlist('ticket_ids')  
        tickets = Ticket.objects.filter(id__in=ticket_ids)  
        cart, created = Cart.objects.get_or_create(user=request.user)  

        if not cart.first_key:
            cart.first_key = generate_key()  
            cart.save()
            
        request.session['ticket_ids'] = ticket_ids 
        context['tickets'] = tickets

        return mock_payment(request)
    else: 
        return redirect('state')  

def mock_payment(request):
    theme = 'panier.css'

    try:
        cart = Cart.objects.get(user=request.user)
        ticket_ids = request.session.get('ticket_ids', [])

        if not ticket_ids:
            return redirect('panier')

        tickets = Ticket.objects.filter(id__in=ticket_ids)
        cart.tickets.add(*tickets)
        cart.save()

        total_price = sum(ticket.price for ticket in cart.tickets.all())
        payment_successful = True  

        if payment_successful:
            user = request.user

            with transaction.atomic():
                cart.second_key = generate_key()
                cart.save()

                for ticket in tickets:
                    ticket.save()
                    
            qr_data = f"{cart.first_key}{cart.second_key}"
            qr = qrcode.make(qr_data)
            qr_io = BytesIO()
            qr.save(qr_io, format='PNG')
            qr_io.seek(0)

            qr_image = ImageReader(qr_io)  

            email = EmailMessage(
                subject="Vos billets pour l'événement",
                body="Voici vos billets en pièce jointe avec le QR code à présenter à l'entrée.",
                to=[user.email],
            )

            for ticket in cart.tickets.all():
                event = ticket.event
                pdf_io = BytesIO()
                p = canvas.Canvas(pdf_io, pagesize=A4)

                width, height = A4
                margin = 2 * cm
                text_start_y = height - margin

                p.setFont("Helvetica", 12)
                p.drawString(margin, text_start_y, "Détails du billet acheté :")
                y_position = text_start_y - 1 * cm
                details = (
                    f"Participation au Jeux Olympiques 2024!\n"
                    f"Billet #{ticket.id}\n"
                    f"Stade : {event.stadium.name}\n"
                    f"Date : {event.date.strftime('%d/%m/%Y')}\n"
                    f"Heure : {event.hour.strftime('%Hh%M')}\n"
                    f"Nom du propriétaire : {user.last_name} {user.first_name}"
                    f"Clé 1 :{cart.first_key}"
                    f"Clé 2 :{cart.second_key}"
                )

                for line in details.split("\n"):
                    p.drawString(margin, y_position, line)
                    y_position -= 0.8 * cm

                qr_size = 4 * cm 
                qr_x = margin
                qr_y = y_position - qr_size - 1 * cm  
                p.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)

                p.save()
                pdf_io.seek(0)

                pdf_filename = f"billet_{ticket.id}.pdf"
                email.attach(pdf_filename, pdf_io.read(), "application/pdf")

            email.send()

            cart.second_key = ""
            cart.save()

            context = {
                'theme': theme,
                'cart': cart,
                'tickets': cart.tickets.all(),
                'total_price': total_price,
                'payment_successful': payment_successful,
            }

            return render(request, 'payment_state.html', context)
        else:
            return render(request, 'payment_state.html', {'theme': theme})

    except Exception as e:
        messages.error(request, f"Une erreur est survenue pendant le traitement de votre demande: {e}")
        return redirect('status')
    
def status(request):
    theme = 'panier.css'
    context = {
        'theme' : theme,
    }

    return render(request, 'payment_state.html', context)

def personal_data(request):
    theme = 'personal_data.css'
    if request.method == "POST":
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            user = request.user
            
            if email and User.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "Cet email est déjà utilisé par un autre utilisateur.")
                return redirect('personal_data')  

            if username and User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà pris.")
                return redirect('personal_data')
            
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email

            user.save()
            messages.success(request, "Vos données personnelles ont été mises à jour.")
            return redirect('personal_data')  

        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de vos données.")
            
    else:
        form = PersonalDataForm(initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    context = {
        'theme': theme,
        'form': form,
        'user': request.user,
    }

    return render(request, 'personal_data.html', context)

def rgpd(request):
    theme = 'documentation.css'
    
    context = {
      'theme': theme,
      'active_page': 'connexion'
    }
    
    return render(request, 'rgpd.html', context)

def cgv(request):
    theme = 'documentation.css'
    
    context = {
      'theme': theme,
      'active_page': 'connexion'
    }
    
    return render(request, 'cgv.html', context)

def cgu(request):
    theme = 'documentation.css'
    
    context = {
      'theme': theme,
      'active_page': 'connexion'
    }
    
    return render(request, 'cgu.html', context)

def mentions(request):
    theme = 'documentation.css'
    
    context = {
      'theme': theme,
      'active_page': 'connexion'
    }
    
    return render(request, 'mentions_legales.html', context)

    