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