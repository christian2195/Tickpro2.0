/* ============================================
   FUNCIONES DE GRUPOS DE CLIENTES
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL GRUPO CLIENTE (Crear/Editar)
    // ==========================================
    var modalGrupo = document.getElementById('modalGrupoCliente');
    if (modalGrupo) {
        modalGrupo.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalGrupoClienteAction');
            var btnGuardar = document.getElementById('btnGuardarGrupoCliente');
            var grupoIdInput = document.getElementById('grupo_cliente_id');

            var form = document.getElementById('formGrupoCliente');
            form.reset();
            form.classList.remove('was-validated');
            grupoIdInput.value = '';

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nuevo';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Crear';
                form.action = '/clientes/grupos/';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Actualizar';
                
                var id = button.getAttribute('data-id');
                var nombre = button.getAttribute('data-nombre');
                var descripcion = button.getAttribute('data-descripcion');
                
                grupoIdInput.value = id;
                document.getElementById('grupo_cliente_nombre').value = nombre;
                document.getElementById('grupo_cliente_descripcion').value = descripcion;
                
                form.action = '/clientes/grupos/editar/' + id + '/';
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR GRUPO
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarGrupoCliente');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarGrupoClienteNombre').textContent = nombre;
            document.getElementById('formEliminarGrupoCliente').action = 
                '/clientes/grupos/eliminar/' + id + '/';
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