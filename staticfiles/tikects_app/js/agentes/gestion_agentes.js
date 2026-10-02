/* ============================================
   FUNCIONES DE GESTIÓN DE AGENTES
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL AGENTE (Crear/Editar)
    // ==========================================
    var modalAgente = document.getElementById('modalAgente');
    if (modalAgente) {
        modalAgente.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalAgenteAction');
            var btnGuardar = document.getElementById('btnGuardarAgente');
            var passwordInput = document.getElementById('password');
            var passwordLabel = document.getElementById('passwordLabel');
            var passwordHelp = document.getElementById('passwordHelp');

            var form = document.getElementById('formAgente');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nuevo';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Crear';
                if (passwordInput) {
                    passwordInput.required = true;
                    passwordInput.placeholder = 'Ingrese una contraseña';
                }
                if (passwordLabel) passwordLabel.innerHTML = 'Contraseña <span class="text-danger">*</span>';
                if (passwordHelp) passwordHelp.style.display = 'block';
                document.getElementById('agente_id').value = '';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Actualizar';
                if (passwordInput) {
                    passwordInput.required = false;
                    passwordInput.placeholder = 'Dejar en blanco para mantener actual';
                }
                if (passwordLabel) passwordLabel.innerHTML = 'Nueva Contraseña';
                if (passwordHelp) passwordHelp.style.display = 'block';

                document.getElementById('agente_id').value = button.getAttribute('data-id');
                document.getElementById('username').value = button.getAttribute('data-username');
                document.getElementById('first_name').value = button.getAttribute('data-first_name');
                document.getElementById('last_name').value = button.getAttribute('data-last_name');
                document.getElementById('email').value = button.getAttribute('data-email');
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR AGENTE
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarAgente');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var username = button.getAttribute('data-username');
            document.getElementById('eliminarAgenteNombre').textContent = username;
            document.getElementById('formEliminarAgente').action = 
                '/gestion/agentes/eliminar/' + id + '/';
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