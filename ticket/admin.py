from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('nbr_place', 'event', 'formula', 'price')
    list_filter = ('event', 'formula')
    search_fields = ('nbr_place', 'event__id')



