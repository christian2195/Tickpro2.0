/* ============================================
   FUNCIONES DE AGENTES GENÉRICOS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL ELIMINAR ASIGNACIÓN GENÉRICA
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarGenerico');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var servicio = button.getAttribute('data-servicio');
            document.getElementById('eliminarGenericoServicio').textContent = servicio;
            document.getElementById('formEliminarGenerico').action = 
                '/gestion/genericos/eliminar/' + id + '/';
        });
    }

    // ==========================================
    // 2. VALIDACIÓN DE FORMULARIOS
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