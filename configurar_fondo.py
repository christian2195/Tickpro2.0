#!/usr/bin/env python3
import os
import shutil
import subprocess

# ==============================================================================
# SCRIPT DE CONFIGURACIÓN DE FONDO PARA TICKPRO 2.0 (VERSION PYTHON)
# ==============================================================================

# Definición de rutas del proyecto
PLANTILLA_LOGIN = "/var/www/html/Tickpro2.0/tikects_app/templates/inicio_sesion_admin.html"
IMAGEN_FONDO = "/var/www/html/Tickpro2.0/tikects_app/static/tikects_app/fondo-inicio.jpg"

print("=== Iniciando configuración del fondo de pantalla (Python) ===")

# 1. Validar existencia de la imagen
if not os.path.exists(IMAGEN_FONDO):
    print(f"❌ ERROR: No se encontró la imagen en: {IMAGEN_FONDO}")
    print("Por favor, sube la imagen con el nombre 'fondo-inicio.jpg' a esa carpeta antes de continuar.")
    exit(1)

# 2. Validar existencia de la plantilla HTML
if not os.path.exists(PLANTILLA_LOGIN):
    print(f"❌ ERROR: No se encontró la plantilla del login en: {PLANTILLA_LOGIN}")
    exit(1)

try:
    # 3. Crear respaldo de seguridad (.bak)
    print("🔄 Creando respaldo de seguridad de la plantilla del login...")
    shutil.copyfile(PLANTILLA_LOGIN, f"{PLANTILLA_LOGIN}.bak")

    # 4. Definir el bloque de estilos CSS a inyectar
    bloque_estilos = """{% load static %}
<style>
    body {
        background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("{% static 'tikects_app/fondo-inicio.jpg' %}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    }
    /* Filtro frosted glass para que la tarjeta resalte */
    .card {
        background-color: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(5px);
        border: none !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
</style>
"""

    # 5. Leer contenido actual del HTML
    print("📝 Leyendo contenido actual del archivo...")
    with open(PLANTILLA_LOGIN, 'r', encoding='utf-8') as archivo_lectura:
        contenido_original = archivo_lectura.read()

    # 6. Escribir el nuevo archivo combinando los estilos y el contenido original
    print("💾 Inyectando estilos y guardando cambios...")
    with open(PLANTILLA_LOGIN, 'w', encoding='utf-8') as archivo_escritura:
        archivo_escritura.write(bloque_estilos + "\n" + contenido_original)

    # 7. Reiniciar Gunicorn mediante la terminal del sistema
    print("🔄 Reiniciando Gunicorn para aplicar los cambios...")
    subprocess.run(["sudo", "systemctl", "restart", "gunicorn"], check=True)

    print("=== ¡Proceso completado con éxito! ===")
    print("Visita http://10.12.12.45/ para ver el nuevo diseño del login.")

except Exception as e:
    print(f"❌ Ocurrió un error inesperado durante el proceso: {e}")
    exit(1)
