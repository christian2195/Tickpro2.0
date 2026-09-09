/* ============================================
   FUNCIONES DE CONFIGURACIÓN
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL GERENCIA (Crear/Editar)
    // ==========================================
    var modalGerencia = document.getElementById('modalGerencia');
    if (modalGerencia) {
        modalGerencia.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalGerenciaAction');
            var btnGuardar = document.getElementById('btnGuardarGerencia');

            var form = document.getElementById('formGerencia');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nueva';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Crear';
                document.getElementById('gerencia_id').value = '';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                if (btnGuardar) btnGuardar.innerHTML = '<i class="fas fa-save me-2"></i> Actualizar';
                document.getElementById('gerencia_id').value = button.getAttribute('data-id');
                document.getElementById('gerencia_nombre').value = button.getAttribute('data-nombre');
                document.getElementById('gerencia_descripcion').value = button.getAttribute('data-descripcion');
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR GERENCIA
    // ==========================================
    var modalEliminar = document.getElementById('modalEliminarGerencia');
    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarGerenciaNombre').textContent = nombre;
            document.getElementById('formEliminarGerencia').action = 
                '/gestion/gerencias/eliminar/' + id + '/';
        });
    }
});