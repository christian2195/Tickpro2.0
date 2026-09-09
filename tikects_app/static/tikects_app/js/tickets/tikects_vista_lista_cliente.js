/* ============================================
   FUNCIONES DE LISTA DE TICKETS DEL CLIENTE
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
    // 2. AUTO-REFRESH OPCIONAL
    // ==========================================
    // setTimeout(function() {
    //     location.reload();
    // }, 30000);
});