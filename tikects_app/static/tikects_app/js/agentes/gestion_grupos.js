/* ============================================
   FUNCIONES DE GESTIÓN DE GRUPOS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. MODAL GRUPO (Crear/Editar)
    // ==========================================
    var modalGrupo = document.getElementById('modalGrupo');
    if (modalGrupo) {
        modalGrupo.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var mode = button.getAttribute('data-mode');
            var actionSpan = document.getElementById('modalGrupoAction');

            var form = document.getElementById('formGrupo');
            form.reset();
            form.classList.remove('was-validated');

            if (mode === 'crear') {
                if (actionSpan) actionSpan.textContent = 'Nuevo';
                document.getElementById('grupo_id').value = '';
            } else if (mode === 'editar') {
                if (actionSpan) actionSpan.textContent = 'Editar';
                var id = button.getAttribute('data-id');
                document.getElementById('grupo_id').value = id;
                document.getElementById('grupo_nombre').value = button.getAttribute('data-nombre');
                document.getElementById('grupo_descripcion').value = button.getAttribute('data-descripcion');
            }
        });
    }

    // ==========================================
    // 2. MODAL ELIMINAR GRUPO
    // ==========================================
    var modalEliminarGrupo = document.getElementById('modalEliminarGrupo');
    if (modalEliminarGrupo) {
        modalEliminarGrupo.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-id');
            var nombre = button.getAttribute('data-nombre');
            document.getElementById('eliminarGrupoNombre').textContent = nombre;
            document.getElementById('formEliminarGrupo').action = 
                '/gestion/grupos/eliminar/' + id + '/';
        });
    }

    // ==========================================
    // 3. MODAL QUITAR AGENTE
    // ==========================================
    var modalQuitar = document.getElementById('modalQuitarAgente');
    if (modalQuitar) {
        modalQuitar.addEventListener('show.bs.modal', function(event) {
            var button = event.relatedTarget;
            var id = button.getAttribute('data-grupo-agente-id');
            var usuario = button.getAttribute('data-usuario');
            var grupo = button.getAttribute('data-grupo');
            document.getElementById('quitarAgenteUsuario').textContent = usuario;
            document.getElementById('quitarAgenteGrupo').textContent = grupo;
            document.getElementById('formQuitarAgente').action = 
                '/gestion/grupos/quitar/' + id + '/';
        });
    }

    // ==========================================
    // 4. VALIDACIÓN DE FORMULARIOS
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