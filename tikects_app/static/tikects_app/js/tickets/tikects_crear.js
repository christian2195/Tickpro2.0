/* ============================================
   FUNCIONES DE CREACIÓN DE TICKETS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. SELECT2 PARA GERENCIA
    // ==========================================
    if (typeof $ !== 'undefined' && $('#gerencia').length) {
        $('#gerencia').select2({
            placeholder: "-- Seleccione o escriba una gerencia --",
            allowClear: true,
            width: '100%'
        });
    }

    // ==========================================
    // 2. VALIDACIÓN DEL FORMULARIO
    // ==========================================
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});