from django.apps import AppConfig


class FleetpingsTemplatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fleetpings_templates'
    verbose_name = 'Fleet Ping Templates'
    
    def ready(self):
        """Hook URLs automatisch ein"""
        self._inject_urls()
    
    def _inject_urls(self):
        """Fügt URLs automatisch zu fleetpings hinzu"""
        try:
            from django.conf import settings
            from django.urls import path
            
            # Prüfe ob fleetpings installiert ist
            if 'fleetpings' not in settings.INSTALLED_APPS:
                return
            
            # Hole fleetpings URLconf
            from importlib import import_module
            fleetpings_urls = import_module('fleetpings.urls')
            
            # Importiere unsere Views
            from . import views
            
            # Füge unsere URLs hinzu
            template_patterns = [
                path('api/templates/', views.list_ping_templates, name='list_ping_templates'),
                path('api/template/<int:template_id>/', views.get_ping_template, name='get_ping_template'),
            ]
            
            if hasattr(fleetpings_urls, 'urlpatterns'):
                # Füge am Ende hinzu
                fleetpings_urls.urlpatterns += template_patterns
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Could not inject URLs into fleetpings: {e}')
