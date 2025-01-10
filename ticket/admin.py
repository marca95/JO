from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'event', 'formula', 'price')
    list_filter = ('event', 'formula')
    search_fields = ('qr_code', 'event__id')



