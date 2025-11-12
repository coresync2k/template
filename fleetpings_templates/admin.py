from django.contrib import admin
from .models import PingTemplate


@admin.register(PingTemplate)
class PingTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'fleet_type',
        'fleet_commander',
        'fleet_doctrine',
        'is_active',
        'created_at'
    )
    
    list_filter = (
        'is_active',
        'fleet_type',
        'created_at'
    )
    
    search_fields = (
        'name',
        'fleet_commander',
        'pre_ping'
    )
    
    fieldsets = (
        ('Allgemein', {
            'fields': ('name', 'is_active', 'webhook')
        }),
        ('Fleet Details', {
            'fields': (
                'fleet_type',
                'fleet_commander',
                'fleet_doctrine',
                'fleet_comms',
                'formup_location'
            )
        }),
        ('Ping Text', {
            'fields': ('pre_ping',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
