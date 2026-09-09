/* ============================================
   FUNCIONES DEL DASHBOARD
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. AUTO-REFRESH OPCIONAL (30 SEGUNDOS)
    // ==========================================
    // Descomentar para habilitar auto-refresh
    // setTimeout(function() {
    //     location.reload();
    // }, 30000);

    // ==========================================
    // 2. ACTUALIZAR ESTADÍSTICAS EN TIEMPO REAL
    // ==========================================
    // Esta función puede ser llamada desde un WebSocket o un setInterval
    // window.actualizarEstadisticas = function() {
    //     fetch('/api/estadisticas/')
    //         .then(response => response.json())
    //         .then(data => {
    //             // Actualizar valores en la UI
    //         })
    //         .catch(error => console.error('Error:', error));
    // };
});