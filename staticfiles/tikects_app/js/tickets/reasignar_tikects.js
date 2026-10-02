/* ============================================
   FUNCIONES DE REASIGNACIÓN DE TICKETS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. VALIDACIÓN DEL FORMULARIO DE REASIGNACIÓN
    // ==========================================
    var form = document.querySelector('form.needs-validation');
    if (form) {
        form.addEventListener('submit', function(event) {
            var select = this.querySelector('select[name="nuevo_agente"]');
            if (select && !select.value) {
                event.preventDefault();
                alert('Debe seleccionar un agente para reasignar el ticket.');
                select.focus();
            }
        });
    }
});