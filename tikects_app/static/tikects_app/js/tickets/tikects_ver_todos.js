/* ============================================
   FUNCIONES DE LISTADO DE TICKETS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. BÚSQUEDA EN TIEMPO REAL
    // ==========================================
    var searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            var filter = this.value.toLowerCase();
            var rows = document.querySelectorAll('#ticketsTable tbody tr');
            
            rows.forEach(function(row) {
                var text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(filter) > -1 ? '' : 'none';
            });
        });
    }

    // ==========================================
    // 2. TOOLTIPS
    // ==========================================
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ==========================================
    // 3. AUTO-REFRESH OPCIONAL
    // ==========================================
    // setTimeout(function() {
    //     location.reload();
    // }, 30000);
});

document.addEventListener('DOMContentLoaded', function() {

    // Función genérica para cargar modales vía Fetch
    function initDynamicModals() {
        const modalContainer = document.getElementById('dynamicModalContainer'); // Contenedor en el HTML base para inyectar el modal
        if (!modalContainer) return;

        // Botones de Detalle
        document.querySelectorAll('.btn-detalle-modal').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const ticketId = this.dataset.id;
                fetch(`/tikects/api/${ticketId}/detalle/`)
                    .then(response => response.text())
                    .then(html => {
                        modalContainer.querySelector('.modal-content').innerHTML = html;
                        const modal = new bootstrap.Modal(modalContainer);
                        modal.show();
                    });
            });
        });

        // Botones de Reasignar
        document.querySelectorAll('.btn-reasignar-modal').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const ticketId = this.dataset.id;
                fetch(`/tikects/api/${ticketId}/reasignar/`)
                    .then(response => response.text())
                    .then(html => {
                        modalContainer.querySelector('.modal-content').innerHTML = html;
                        const modal = new bootstrap.Modal(modalContainer);
                        modal.show();
                        
                        // Manejar el submit del form de reasignación vía AJAX
                        const form = modalContainer.querySelector('#formReasignarModal');
                        if(form){
                            form.addEventListener('submit', function(ev) {
                                ev.preventDefault();
                                const formData = new FormData(form);
                                fetch(form.action, {
                                    method: 'POST',
                                    body: formData,
                                    headers: {
                                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                                    }
                                }).then(res => {
                                    if(res.ok){
                                        modal.hide();
                                        location.reload(); // Opcional: recargar la tabla sin refrescar toda la página
                                    }
                                });
                            });
                        }
                    });
            });
        });
    }

    initDynamicModals();
});