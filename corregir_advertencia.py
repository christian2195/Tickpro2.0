import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos la línea exacta que genera la advertencia desordenada
    linea_vieja = "clientes_list = Cliente.objects.all()"
    linea_nueva = "clientes_list = Cliente.objects.all().order_by('nombre')"

    if linea_vieja in contenido:
        nuevo_contenido = contenido.replace(linea_vieja, linea_nueva)
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡views.py actualizado! Consulta de clientes ordenada de forma consistente.")
    else:
        print("❌ No se encontró la línea exacta en views.py (puede que ya esté modificada).")
else:
    print("❌ No se encontró el archivo tikects_app/views.py")
