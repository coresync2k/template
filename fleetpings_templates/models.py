from django.db import models
from django.utils.translation import gettext_lazy as _


class PingTemplate(models.Model):
    """Template für Fleet Pings - referenziert fleetpings Models dynamisch"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Template Name"),
        help_text=_("Name für diese Vorlage")
    )
    
    fleet_type = models.ForeignKey(
        'fleetpings.FleetType',  # String-Referenz für Lazy Loading
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Fleet Type")
    )
    
    fleet_commander = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Fleet Commander")
    )
    
    fleet_doctrine = models.ForeignKey(
        'fleetpings.FleetDoctrine',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Doctrine")
    )
    
    fleet_comms = models.ForeignKey(
        'fleetpings.FleetComms',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Comms")
    )
    
    formup_location = models.ForeignKey(
        'fleetpings.FormupLocation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Formup Location")
    )
    
    webhook = models.ForeignKey(
        'fleetpings.Webhook',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Webhook"),
        help_text=_("Ziel-Webhook für dieses Template")
    )
    
    pre_ping = models.TextField(
        blank=True,
        verbose_name=_("Pre-Ping Text"),
        help_text=_("Text vor dem Ping")
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Aktiv"),
        help_text=_("Inaktive Templates werden nicht angezeigt")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Erstellt am")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Aktualisiert am")
    )
    
    class Meta:
        verbose_name = _("Ping Template")
        verbose_name_plural = _("Ping Templates")
        ordering = ['name']
        app_label = 'fleetpings_templates'
    
    def __str__(self):
        return self.name
