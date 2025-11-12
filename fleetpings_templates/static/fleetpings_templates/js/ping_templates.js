/**
 * JavaScript für Ping Templates - Auto-Load Version
 * Injiziert sich automatisch in aa-fleetpings
 */

(function() {
    'use strict';
    
    // Warte bis jQuery und DOM ready sind
    if (typeof jQuery === 'undefined') {
        console.warn('jQuery not loaded, retrying...');
        setTimeout(arguments.callee, 100);
        return;
    }
    
    $(document).ready(function() {
        // Prüfe ob wir auf der Ping-Erstellungsseite sind
        if (!isFleetPingCreatePage()) {
            return;
        }
        
        // Templates laden und in die Sidebar einfügen
        loadAndInjectTemplates();
        
        // Event-Handler für Template-Auswahl
        $(document).on('click', '.ping-template-item', function(e) {
            e.preventDefault();
            const templateId = $(this).data('template-id');
            loadTemplate(templateId);
        });
    });
    
    /**
     * Prüft ob wir auf der richtigen Seite sind
     */
    function isFleetPingCreatePage() {
        // Suche nach typischen Elementen des Ping-Formulars
        return $('#id_webhook, select[name="webhook"]').length > 0 ||
               $('#id_fleet_type, select[name="fleet_type"]').length > 0;
    }
    
    /**
     * Lädt Templates und fügt sie in die Sidebar ein
     */
    function loadAndInjectTemplates() {
        $.ajax({
            url: '/fleetpings/api/templates/',
            type: 'GET',
            success: function(response) {
                if (response.success && response.templates && response.templates.length > 0) {
                    injectTemplatePanel(response.templates);
                }
            },
            error: function(xhr, status, error) {
                console.error('Fehler beim Laden der Templates:', error);
            }
        });
    }
    
    /**
     * Fügt Template-Panel in die Sidebar ein
     */
    function injectTemplatePanel(templates) {
        const templatePanel = `
            <div class="panel panel-default ping-templates-panel">
                <div class="panel-heading">
                    <h3 class="panel-title">
                        <i class="fas fa-file-alt"></i> Vorlagen
                    </h3>
                </div>
                <div class="panel-body">
                    <div class="list-group">
                        ${templates.map(t => `
                            <a href="#" class="list-group-item ping-template-item" data-template-id="${t.id}">
                                <i class="fas fa-clone"></i> ${escapeHtml(t.name)}
                            </a>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        // Finde Sidebar (verschiedene Möglichkeiten)
        const sidebar = $('.fleetpings-sidebar, .col-md-3, .sidebar, [class*="sidebar"]').first();
        
        if (sidebar.length > 0) {
            sidebar.prepend(templatePanel);
        } else {
            // Fallback: Füge rechts vom Formular ein
            $('form').first().closest('.row').append(`
                <div class="col-md-3">
                    ${templatePanel}
                </div>
            `);
        }
    }
    
    /**
     * Lädt ein bestimmtes Template und füllt das Formular
     */
    function loadTemplate(templateId) {
        $.ajax({
            url: `/fleetpings/api/template/${templateId}/`,
            type: 'GET',
            success: function(response) {
                if (response.success && response.data) {
                    fillFormWithTemplate(response.data);
                }
            },
            error: function(xhr, status, error) {
                console.error('Fehler beim Laden des Templates:', error);
                alert('Fehler beim Laden der Vorlage. Bitte versuchen Sie es erneut.');
            }
        });
    }
    
    /**
     * Füllt das Formular mit Template-Daten
     */
    function fillFormWithTemplate(data) {
        // Webhook
        if (data.webhook) {
            $('#id_webhook, select[name="webhook"]').val(data.webhook).trigger('change');
        }
        
        // Fleet Type
        if (data.fleet_type) {
            $('#id_fleet_type, select[name="fleet_type"]').val(data.fleet_type).trigger('change');
        }
        
        // Fleet Commander
        if (data.fleet_commander) {
            $('#id_fleet_commander, input[name="fleet_commander"]').val(data.fleet_commander);
        }
        
        // Doctrine
        if (data.fleet_doctrine) {
            $('#id_fleet_doctrine, select[name="fleet_doctrine"]').val(data.fleet_doctrine).trigger('change');
        }
        
        // Comms
        if (data.fleet_comms) {
            $('#id_fleet_comms, select[name="fleet_comms"]').val(data.fleet_comms).trigger('change');
        }
        
        // Formup Location
        if (data.formup_location) {
            $('#id_formup_location, select[name="formup_location"]').val(data.formup_location).trigger('change');
        }
        
        // Pre-Ping Text
        if (data.pre_ping) {
            $('#id_pre_ping, textarea[name="pre_ping"]').val(data.pre_ping);
        }
        
        // Visual Feedback
        showNotification('Vorlage geladen!', 'success');
    }
    
    /**
     * Zeigt eine Benachrichtigung an
     */
    function showNotification(message, type) {
        const alertClass = type === 'success' ? 'alert-success' : 'alert-info';
        const notification = $(`
            <div class="alert ${alertClass} alert-dismissible fade in" role="alert" 
                 style="position: fixed; top: 70px; right: 20px; z-index: 9999; min-width: 250px;">
                ${escapeHtml(message)}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(function() {
            notification.fadeOut(function() {
                $(this).remove();
            });
        }, 3000);
    }
    
    /**
     * Escaped HTML für XSS-Schutz
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }
    
})();
