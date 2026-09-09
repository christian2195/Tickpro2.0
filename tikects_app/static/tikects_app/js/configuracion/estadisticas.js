/* ============================================
   FUNCIONES DE ESTADÍSTICAS
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. GRÁFICO: Estado de tickets (Pie)
    // ==========================================
    const statusCtx = document.getElementById('tikectsStatusChart');
    if (statusCtx) {
        const statusData = JSON.parse(statusCtx.dataset.data || '{"labels":["Abiertos","Cerrados"],"data":[0,0]}');
        new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: statusData.labels || ['Abiertos', 'Cerrados'],
                datasets: [{
                    data: statusData.data || [0, 0],
                    backgroundColor: ['#28a745', '#dc3545'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    // ==========================================
    // 2. GRÁFICO: Tickets por Servicio (Barra)
    // ==========================================
    const serviceCtx = document.getElementById('tikectsServiceChart');
    if (serviceCtx) {
        const serviceData = JSON.parse(serviceCtx.dataset.data || '{"labels":[],"data":[]}');
        new Chart(serviceCtx, {
            type: 'bar',
            data: {
                labels: serviceData.labels || [],
                datasets: [{
                    label: 'Cantidad de Tickets',
                    data: serviceData.data || [],
                    backgroundColor: '#17a2b8',
                    borderColor: '#138496',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
    }

    // ==========================================
    // 3. GRÁFICO: Tickets por Prioridad (Doughnut)
    // ==========================================
    const prioridadCtx = document.getElementById('prioridadChart');
    if (prioridadCtx) {
        const prioridadData = JSON.parse(prioridadCtx.dataset.data || '{"labels":[],"data":[]}');
        new Chart(prioridadCtx, {
            type: 'doughnut',
            data: {
                labels: prioridadData.labels || [],
                datasets: [{
                    data: prioridadData.data || [],
                    backgroundColor: ['#17a2b8', '#ffc107', '#fd7e14', '#dc3545', '#6c757d']
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }

    // ==========================================
    // 4. GRÁFICO: Tickets Cerrados por Día (Línea)
    // ==========================================
    const diaCtx = document.getElementById('tikectsPorDiaCerradosChart');
    if (diaCtx) {
        const diaData = JSON.parse(diaCtx.dataset.data || '{"labels":[],"data":[]}');
        new Chart(diaCtx, {
            type: 'line',
            data: {
                labels: diaData.labels || [],
                datasets: [{
                    label: 'Tickets Cerrados',
                    data: diaData.data || [],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
    }

    // ==========================================
    // 5. GRÁFICO: Tickets Cerrados por Mes (Barra)
    // ==========================================
    const mesCtx = document.getElementById('tikectsPorMesCerradosChart');
    if (mesCtx) {
        const mesData = JSON.parse(mesCtx.dataset.data || '{"labels":[],"data":[]}');
        new Chart(mesCtx, {
            type: 'bar',
            data: {
                labels: mesData.labels || [],
                datasets: [{
                    label: 'Tickets Cerrados',
                    data: mesData.data || [],
                    backgroundColor: '#007bff',
                    borderColor: '#0056b3',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
    }

    // ==========================================
    // 6. GRÁFICO: Tickets Cerrados por Semana (Línea)
    // ==========================================
    const semanaCtx = document.getElementById('tikectsPorSemanaCerradosChart');
    if (semanaCtx) {
        const semanaData = JSON.parse(semanaCtx.dataset.data || '{"labels":[],"data":[]}');
        new Chart(semanaCtx, {
            type: 'line',
            data: {
                labels: semanaData.labels || [],
                datasets: [{
                    label: 'Tickets Cerrados',
                    data: semanaData.data || [],
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 } }
                }
            }
        });
    }
});