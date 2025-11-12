"""Context Processor um Templates automatisch einzubinden"""


def inject_templates(request):
    """
    Fügt Template-Include automatisch hinzu wenn auf fleetpings Seite
    """
    # Prüfe ob wir auf einer fleetpings URL sind
    if request.path.startswith('/fleetpings/'):
        return {
            'load_ping_templates': True
        }
    return {}
