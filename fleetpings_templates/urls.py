from django.urls import path
from . import views

app_name = 'fleetpings_templates'

urlpatterns = [
    path('api/templates/', views.list_ping_templates, name='list_ping_templates'),
    path('api/template/<int:template_id>/', views.get_ping_template, name='get_ping_template'),
]
