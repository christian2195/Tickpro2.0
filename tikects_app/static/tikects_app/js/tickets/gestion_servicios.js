/* ============================================
   FUNCIONES DE GESTIÓN DE SERVICIOS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL SERVICIO (Crear/Editar)
    // ==========================================
    var modalServicio = document.getElementById('modalServicio');
    if (modalServicio) {
        modalServicio.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalServicioAction');

            var form = document.getElementById('formServicio');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nuevo';
                document.getElementById('servicio_id').value = '';
                form.action = '/gestion/servicios/';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                var id = button.getAttribute('data-id');
                document.getElementById('servicio_id').value = id;
                document.getElementById('servicio_nombre').value = button.getAttribute('data-nombre');
                document.getElementById('servicio_descripcion').value = button.getAttribute('data-descripcion');
                form.action = '/servicios/editar/' + id + '/';
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR SERVICIO
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarServicio');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarServicioNombre').textContent = nombre;
            document.getElementById('formEliminarServicio').action = 
                '/servicios/eliminar/' + id + '/';
        });
    }

    // ==========================================
    // 3. VALIDACIÓN DE FORMULARIOS
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