/* ============================================
   FUNCIONES DE GESTIÓN DE CLIENTES
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL CLIENTE (Crear/Editar)
    // ==========================================
    var modalCliente = document.getElementById('modalCliente');
    if (modalCliente) {
        modalCliente.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalClienteAction');
            var passwordInput = document.getElementById('cliente_password');
            var passwordRequiredAsterisk = document.getElementById('cliente_password_required');

            var form = document.getElementById('formCliente');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Alta de';
                document.getElementById('cliente_id').value = '';
                // CORRECCIÓN AQUÍ: Apunta a la ruta correcta definida en urls.py
                form.action = '/clientes/crear/'; 
                
                // En creación, la clave es obligatoria
                passwordInput.required = true;
                if (passwordRequiredAsterisk) passwordRequiredAsterisk.style.display = 'inline';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Modificar';
                var id = button.getAttribute('data-id');
                document.getElementById('cliente_id').value = id;
                document.getElementById('cliente_nombre').value = button.getAttribute('data-nombre');
                document.getElementById('cliente_apellido').value = button.getAttribute('data-apellido');
                document.getElementById('cliente_username').value = button.getAttribute('data-username');
                document.getElementById('cliente_email').value = button.getAttribute('data-email');
                document.getElementById('cliente_telefono').value = button.getAttribute('data-telefono');
                document.getElementById('cliente_gerencia').value = button.getAttribute('data-gerencia');
                
                form.action = '/clientes/editar/' + id + '/';
                
                // En edición, la clave es opcional
                passwordInput.required = false;
                if (passwordRequiredAsterisk) passwordRequiredAsterisk.style.display = 'none';
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR CLIENTE
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarCliente');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarClienteNombre').textContent = nombre;
            document.getElementById('formEliminarCliente').action = 
                '/clientes/eliminar/' + id + '/';
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