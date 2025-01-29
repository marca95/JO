from django.contrib import admin
from django.db.models import Count
from ticket.models import Ticket
from panier.models import Cart

class TicketAdmin(admin.ModelAdmin):
    list_display = ('nbr_place', 'event', 'formula', 'price', 'total_sales')
    list_filter = ('event', 'formula', 'nbr_place', 'price')
    search_fields = ('nbr_place', 'event__id', 'formula')

    def total_sales(self, obj):
        total = Cart.objects.filter(tickets=obj).aggregate(total=Count('tickets'))['total'] or 0  
        return total

admin.site.register(Ticket, TicketAdmin)
