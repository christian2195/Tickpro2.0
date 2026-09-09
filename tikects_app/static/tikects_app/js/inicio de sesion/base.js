/* ============================================
   FUNCIONES BASE PARA INICIO DE SESIÓN
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. TOOLTIPS
    // ==========================================
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ==========================================
    // 2. VALIDACIÓN DE FORMULARIOS BOOTSTRAP
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

    // ==========================================
    // 3. AUTO-CERRAR ALERTAS DESPUÉS DE 5 SEGUNDOS
    // ==========================================
    var alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            var closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });

    // ==========================================
    // 4. FUNCIÓN PARA CONFIRMAR ELIMINACIONES
    // ==========================================
    window.confirmarEliminacion = function(event, mensaje) {
        if (!confirm(mensaje || '¿Estás seguro de que deseas eliminar este elemento?')) {
            event.preventDefault();
            return false;
        }
        return true;
    };

    // ==========================================
    // 5. LOADING BUTTON
    // ==========================================
    window.showLoading = function(buttonId, textId, spinnerId) {
        var button = document.getElementById(buttonId);
        var text = document.getElementById(textId);
        var spinner = document.getElementById(spinnerId);
        
        if (button) button.disabled = true;
        if (text) text.classList.add('d-none');
        if (spinner) spinner.classList.remove('d-none');
    };

    window.hideLoading = function(buttonId, textId, spinnerId) {
        var button = document.getElementById(buttonId);
        var text = document.getElementById(textId);
        var spinner = document.getElementById(spinnerId);
        
        if (button) button.disabled = false;
        if (text) text.classList.remove('d-none');
        if (spinner) spinner.classList.add('d-none');
    };

    // ==========================================
    // 6. FUNCIÓN PARA OBTENER PARÁMETROS DE URL
    // ==========================================
    window.getUrlParameter = function(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    };

    // ==========================================
    // 7. FUNCIÓN PARA BÚSQUEDA EN TABLAS
    // ==========================================
    window.buscarEnTabla = function(inputId, tableId) {
        var input = document.getElementById(inputId);
        if (!input) return;
        
        input.addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var rows = document.querySelectorAll('#' + tableId + ' tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(filter) > -1 ? '' : 'none';
            });
        });
    };
});