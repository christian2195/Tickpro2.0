/* ============================================
   FUNCIONES DE GESTIÓN DE RESPUESTAS AUTOMÁTICAS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL ELIMINAR RESPUESTA
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarRespuesta');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarRespuestaNombre').textContent = nombre;
            document.getElementById('formEliminarRespuesta').action = 
                '/gestion/respuestas/eliminar/' + id + '/';
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