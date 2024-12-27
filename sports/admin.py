from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('date', 'hour', 'stadium', 'sport')
    list_filter = ('stadium', 'sport', 'date')
    search_fields = ('stadium__name', 'sport__name')
    ordering = ('date', 'hour')
