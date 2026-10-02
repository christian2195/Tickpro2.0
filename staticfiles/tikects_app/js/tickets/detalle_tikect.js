/* ============================================
   FUNCIONES DE DETALLE DE TICKET
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. VALIDACIÓN DEL FORMULARIO DE CIERRE
    // ==========================================
    var cerrarForm = document.querySelector('#cerrarModal form');
    if (cerrarForm) {
        cerrarForm.addEventListener('submit', function(event) {
            var textarea = this.querySelector('textarea[name="descripcion_solucion"]');
            if (textarea && textarea.value.trim() === '') {
                event.preventDefault();
                alert('Debe ingresar una descripción de la solución antes de cerrar el ticket.');
                textarea.focus();
            }
        });
    }

    // ==========================================
    // 2. CONFIRMAR CIERRE DEL TICKET
    // ==========================================
    var cerrarBtn = document.querySelector('[data-bs-target="#cerrarModal"]');
    if (cerrarBtn) {
        cerrarBtn.addEventListener('click', function() {
            var ticketId = this.getAttribute('data-ticket-id') || '';
            // Puedes usar el ticketId si es necesario
        });
    }
});