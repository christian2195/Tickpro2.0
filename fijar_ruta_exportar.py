import os

ruta_urls = os.path.join('tikects_app', 'urls.py')

if os.path.exists(ruta_urls):
    with open(ruta_urls, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Definimos la línea exacta que queremos agregar
    nueva_ruta = "    path('clientes/exportar-excel/', views.exportar_usuarios_excel, name='exportar_excel'),"

    # Verificamos si la ruta ya existe para no duplicarla
    if "name='exportar_excel'" in contenido or "name=\"exportar_excel\"" in contenido:
        print("💡 La ruta 'exportar_excel' ya parece existir en tu urls.py.")
    else:
        # Buscamos la ruta de registrar_usuarios para meter la nueva justo debajo
        if "name='registrar_usuarios'" in contenido:
            contenido = contenido.replace(
                "name='registrar_usuarios'),",
                "name='registrar_usuarios'),\n" + nueva_ruta
            )
            with open(ruta_urls, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print("✅ ¡urls.py actualizado! Se vinculó la ruta 'exportar_excel' con éxito.")
        elif 'name="registrar_usuarios"' in contenido:
            contenido = contenido.replace(
                'name="registrar_usuarios"),',
                'name="registrar_usuarios"),\n' + nueva_ruta
            )
            with open(ruta_urls, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print("✅ ¡urls.py actualizado! Se vinculó la ruta 'exportar_excel' con éxito.")
        else:
            print("❌ No se encontró la ruta de 'registrar_usuarios' para usarla como punto de referencia.")
else:
    print("❌ No se encontró el archivo tikects_app/urls.py")
