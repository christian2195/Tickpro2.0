/* ============================================
   TICKPRO - CONTROLADOR DE MODALES HÍBRIDOS (FETCH API)
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    const modalContainerEl = document.getElementById('dynamicTicketModal');
    if (!modalContainerEl) return;
    
    const dynamicModal = new bootstrap.Modal(modalContainerEl);
    const modalContent = modalContainerEl.querySelector('.modal-content');

    // Muestra un loader limpio mientras se hace el Fetch
    const showLoader = () => {
        modalContent.innerHTML = `
            <div class="p-5 text-center">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-3 tp-caption text-muted">Consultando registro...</p>
            </div>
        `;
        dynamicModal.show();
    };

    // 1. Delegación de eventos para Abrir Modales
    document.body.addEventListener('click', function(e) {
        
        // --- MODAL DETALLE ---
        const btnDetalle = e.target.closest('.btn-detalle-modal');
        if (btnDetalle) {
            e.preventDefault();
            showLoader();
            // CORRECCIÓN: Ruta exacta alineada con urls.py (/api/tickets/...)
            fetch(`/api/tickets/${btnDetalle.dataset.id}/detalle/`)
                .then(res => {
                    if (!res.ok) throw new Error("Acceso denegado o ticket inexistente.");
                    return res.text();
                })
                .then(html => modalContent.innerHTML = html)
                .catch(err => modalContent.innerHTML = `<div class="p-4 text-danger">${err.message}</div>`);
        }

        // --- MODAL REASIGNAR ---
        const btnReasignar = e.target.closest('.btn-reasignar-modal');
        if (btnReasignar) {
            e.preventDefault();
            showLoader();
            // CORRECCIÓN: Ruta exacta alineada con urls.py (/api/tickets/...)
            fetch(`/api/tickets/${btnReasignar.dataset.id}/reasignar/`)
                .then(res => {
                    if (!res.ok) throw new Error("Permisos insuficientes.");
                    return res.text();
                })
                .then(html => modalContent.innerHTML = html)
                .catch(err => modalContent.innerHTML = `<div class="p-4 text-danger">${err.message}</div>`);
        }
    });

    // 2. Manejo de Submits vía AJAX dentro del modal dinámico (Reasignación)
    modalContainerEl.addEventListener('submit', function(e) {
        const form = e.target;
        if (form.classList.contains('ajax-form')) {
            e.preventDefault();
            
            // UI Feedback
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Procesando...';
            submitBtn.disabled = true;

            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    dynamicModal.hide();
                    location.reload(); // Refresca para actualizar la tabla y mostrar el badge
                } else {
                    alert('Error: ' + data.message);
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            })
            .catch(err => {
                alert('Ocurrió un error de red.');
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        }
    });
});