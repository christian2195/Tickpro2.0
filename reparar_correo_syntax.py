import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos el segmento exacto que está mal estructurado y lo corregimos con triples comillas
    linea_con_error = 'f"Hola {tikect.usuario.first_name},'
    
    # Reemplazamos la lógica de la función cerrar_tikect para asegurar que el string cierre perfecto
    viejo_bloque_mensaje = """            asunto = f"Ticket Cerrado: #{tikect.id} - {tikect.titulo}"
            mensaje = (
                f"Hola {tikect.usuario.first_name},
                f"Tu ticket ha sido marcado como CERRADO.\\n"
                f"Solución aplicada: {descripcion_solucion}\\n\\n"
                f"Gracias por contactarnos."
            )"""

    nuevo_bloque_mensaje = """            asunto = f"Ticket Cerrado: #{tikect.id} - {tikect.titulo}"
            mensaje = (
                f"Hola {tikect.usuario.first_name},\\n\\n"
                f"Tu ticket ha sido marcado como CERRADO.\\n"
                f"Solución aplicada: {descripcion_solucion}\\n\\n"
                f"Gracias por contactarnos."
            )"""

    if viejo_bloque_mensaje in contenido:
        contenido = contenido.replace(viejo_bloque_mensaje, nuevo_bloque_mensaje)
    else:
        # Intento de corrección más directo si los espacios varían
        contenido = contenido.replace('f"Hola {tikect.usuario.first_name},', 'f"Hola {tikect.usuario.first_name},\\n"')

    with open(ruta_views, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ ¡Error de sintaxis en f-string reparado con éxito en views.py!")
else:
    print("❌ No se encontró el archivo views.py")
