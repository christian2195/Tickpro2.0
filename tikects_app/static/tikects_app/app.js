// Función para agregar la animación a la campana y mostrar el punto rojo
function animateBell() {
    const bell = document.querySelector('.notification-bell');
    if (bell) {
        bell.classList.add('animated', 'has-notification');
        setTimeout(() => {
            bell.classList.remove('animated');
        }, 1000); // Duración de la animación
    }
}

// Función para actualizar el contenido del menú de notificaciones
function updateNotifications(notifications) {
    const dropdownMenu = document.querySelector('#navbarDropdown + .dropdown-menu');
    dropdownMenu.innerHTML = ''; // Vaciar el contenido actual

    notifications.forEach(notification => {
        const notificationItem = document.createElement('li');
        notificationItem.classList.add('dropdown-item');
        notificationItem.innerHTML = `
            <div class="notification-content">
                <span><a href="/tikects/detalles/${notification.tikect_id}">${notification.descripcion}</a></span>
            </div>
        `;
        dropdownMenu.appendChild(notificationItem);
    });
}

// Crear un objeto de audio para el sonido de notificación
const notificationSound = new Audio('/static/tikects_app/notification.mp3');

// Función para verificar nuevas notificaciones
let lastNotificationCount = 0; // Variable para rastrear el número de notificaciones previas

function checkForNotifications() {
    fetch('/path/to/your/notification/api/') // Cambia esta URL por tu endpoint real
        .then(response => response.json())
        .then(data => {
            if (data.new_notifications) {
                const currentNotificationCount = data.notifications.length;

                // Reproducir sonido solo si hay nuevas notificaciones
                if (currentNotificationCount > lastNotificationCount) {
                    animateBell();
                    updateNotifications(data.notifications);
                    notificationSound.play().catch(error => {
                        console.error('Error al reproducir el sonido:', error);
                    });
                }

                // Actualizar el conteo de notificaciones
                lastNotificationCount = currentNotificationCount;
            }
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// Realizar la consulta periódica cada cierto tiempo
document.addEventListener('DOMContentLoaded', (event) => {
    setInterval(checkForNotifications, 10000); // Cada 10 segundos
});