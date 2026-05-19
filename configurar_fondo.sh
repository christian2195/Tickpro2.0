#!/bin/bash

# ==============================================================================
# SCRIPT DE CONFIGURACIÓN DE FONDO PARA TICKPRO 2.0
# ==============================================================================

# Rutas del proyecto
PLANTILLA_LOGIN="/var/www/html/Tickpro2.0/tikects_app/templates/inicio_sesion_admin.html"
IMAGEN_FONDO="/var/www/html/Tickpro2.0/tikects_app/static/tikects_app/fondo-inicio.jpg"

echo "=== Iniciando configuración del fondo de pantalla ==="

# 1. Verificar si la imagen de fondo existe
if [ ! -f "$IMAGEN_FONDO" ]; then
    echo "❌ ERROR: No se encontró la imagen en: $IMAGEN_FONDO"
    echo "Por favor, sube la imagen con el nombre 'fondo-inicio.jpg' a esa carpeta antes de continuar."
    exit 1
fi

# 2. Verificar si la plantilla HTML existe
if [ ! -f "$PLANTILLA_LOGIN" ]; then
    echo "❌ ERROR: No se encontró la plantilla del login en: $PLANTILLA_LOGIN"
    exit 1
fi

# 3. Crear un respaldo de seguridad de la plantilla actual
echo "🔄 Creando respaldo de seguridad de la plantilla del login..."
cp "$PLANTILLA_LOGIN" "${PLANTILLA_LOGIN}.bak"

# 4. Definir el bloque de estilos CSS a inyectar
# Nota: Usa el tag {% load static %} si no está cargado, y define el background con filtro oscuro
BLOQUE_ESTILOS=$(cat << 'EOF'
{% load static %}
<style>
    body {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{% static 'tikects_app/fondo-inicio.jpg' %}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    }
    /* Estilo extra para asegurar que la tarjeta de login resalte sobre el fondo */
    .card {
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(5px);
        border: none !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
</style>
EOF
)

# 5. Inyectar el bloque de estilos al principio del archivo HTML de forma limpia
echo "📝 Inyectando estilos CSS en la plantilla HTML..."
echo -e "$BLOQUE_ESTILOS\n$(cat $PLANTILLA_LOGIN)" > "$PLANTILLA_LOGIN"

# 6. Reiniciar Gunicorn para aplicar los cambios en producción
echo "🔄 Reiniciando Gunicorn para vaciar caché..."
sudo systemctl restart gunicorn

echo "=== ¡Proceso completado con éxito! ==="
echo "Visita http://10.12.12.45/ para ver tu nueva pantalla de inicio estilizada."
