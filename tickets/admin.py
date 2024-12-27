from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'owner', 'stadium', 'formula', 'price')
    list_filter = ('stadium', 'formula')
    search_fields = ('qr_code', 'owner__username', 'stadium__name')



