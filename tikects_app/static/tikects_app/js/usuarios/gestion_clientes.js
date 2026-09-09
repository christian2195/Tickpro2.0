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
            var btnGuardar = document.getElementById('btnGuardarCliente');
            var passwordInput = document.getElementById('cliente_password');
            var passwordRequired = document.getElementById('cliente_password_required');
            var passwordFeedback = document.getElementById('cliente_password_feedback');

            var form = document.getElementById('formCliente');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nuevo';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Crear';
                document.getElementById('cliente_id').value = '';
                if (passwordInput) {
                    passwordInput.required = true;
                    passwordInput.placeholder = 'Ingrese una contraseña';
                }
                if (passwordRequired) passwordRequired.textContent = '*';
                if (passwordFeedback) passwordFeedback.textContent = 'La contraseña es obligatoria para nuevos usuarios.';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Actualizar';
                document.getElementById('cliente_id').value = button.getAttribute('data-id');
                document.getElementById('cliente_nombre').value = button.getAttribute('data-nombre');
                document.getElementById('cliente_apellido').value = button.getAttribute('data-apellido');
                document.getElementById('cliente_username').value = button.getAttribute('data-username');
                document.getElementById('cliente_email').value = button.getAttribute('data-email') || '';
                document.getElementById('cliente_telefono').value = button.getAttribute('data-telefono') || '';
                document.getElementById('cliente_gerencia').value = button.getAttribute('data-gerencia') || '';
                if (passwordInput) {
                    passwordInput.required = false;
                    passwordInput.placeholder = 'Dejar en blanco para mantener actual';
                }
                if (passwordRequired) passwordRequired.textContent = '(opcional)';
                if (passwordFeedback) passwordFeedback.textContent = 'Solo complete si desea cambiar la contraseña.';
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