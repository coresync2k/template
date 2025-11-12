from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from .models import PingTemplate


@login_required
@permission_required('fleetpings.basic_access')
@require_http_methods(["GET"])
def get_ping_template(request, template_id):
    """Gibt Template-Daten als JSON zurück"""
    try:
        template = PingTemplate.objects.get(id=template_id, is_active=True)
        
        data = {
            'webhook': template.webhook.id if template.webhook else None,
            'fleet_type': template.fleet_type.id if template.fleet_type else None,
            'fleet_commander': template.fleet_commander,
            'fleet_doctrine': template.fleet_doctrine.id if template.fleet_doctrine else None,
            'fleet_comms': template.fleet_comms.id if template.fleet_comms else None,
            'formup_location': template.formup_location.id if template.formup_location else None,
            'pre_ping': template.pre_ping,
        }
        
        return JsonResponse({'success': True, 'data': data})
    
    except PingTemplate.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Template nicht gefunden'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@permission_required('fleetpings.basic_access')
@require_http_methods(["GET"])
def list_ping_templates(request):
    """Gibt eine Liste aller aktiven Templates zurück"""
    try:
        templates = PingTemplate.objects.filter(is_active=True).values('id', 'name')
        
        return JsonResponse({
            'success': True,
            'templates': list(templates)
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
