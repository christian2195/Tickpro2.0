/* ============================================
   FUNCIONES DE TICKETS ASIGNADOS A AGENTES
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. TOOLTIPS
    // ==========================================
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ==========================================
    // 2. AUTO-REFRESH (30 SEGUNDOS)
    // ==========================================
    // Descomentar para habilitar auto-refresh
    // setTimeout(function() {
    //     location.reload();
    // }, 30000);

    // ==========================================
    // 3. CONFIRMAR CIERRE DE TICKET
    // ==========================================
    var cerrarBtns = document.querySelectorAll('[data-bs-target^="#cerrarModal"]');
    cerrarBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var ticketId = this.getAttribute('data-ticket-id') || '';
            // Puedes usar el ticketId si es necesario
        });
    });
});