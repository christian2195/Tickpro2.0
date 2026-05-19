import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Bloque de código optimizado con mapeo explícito de campos individuales
    codigo_campos_fijo = """                    # Extraemos y limpiamos los valores del Excel
                    txt_nombre = str(row['Nombre']).strip()
                    txt_apellido = str(row['Apellido']).strip()
                    username_field = str(row['usuario']).strip()
                    
                    # Creamos el perfil de Cliente adaptándonos dinámicamente a los campos reales del modelo
                    nombre_completo = f"{txt_nombre} {txt_apellido}"
                    
                    campos_posibles = {
                        'nombre': nombre_completo,
                        'primer_nombre': txt_nombre,
                        'primer_apellido': txt_apellido,
                        'apellido': txt_apellido,        # Mapeo directo para corregir la columna vacía
                        'nombre_usuario': username_field, # Mapeo directo para el nombre de usuario
                        'usuario_nombre': username_field,
                        'correo': correo_automatico,
                        'email': correo_automatico,
                        'telefono': '000-000-0000',
                        'gerencia': gerencia_obj,
                        'direccion': row['Direccion'],
                        'usuario': user,                  # Enlace de la relación de Django
                    }
                    
                    import inspect
                    campos_reales = [f.name for f in Cliente._meta.get_fields()]
                    
                    argumentos_validos = {
                        k: v for k, v in campos_posibles.items() 
                        if k in campos_reales
                    }
                    
                    if 'rif' in campos_reales:
                        argumentos_validos['rif'] = f"V-{user.id:08d}"
                    elif 'cedula' in campos_reales:
                        argumentos_validos['cedula'] = f"{user.id:08d}"
                        
                    Cliente.objects.create(**argumentos_validos)
                    usuarios_creados += 1"""

    # Localizamos el bloque dinámico anterior para inyectar las variables separadas de nombre/apellido
    if "nombre_completo = f\"{row['Nombre']} {row['Apellido']}\"" in contenido:
        # Hacemos una segmentación quirúrgica del archivo views.py para sustituir la lógica vieja
        partes = contenido.split("nombre_completo = f\"{row['Nombre']} {row['Apellido']}\"")
        resto = partes[1].split("usuarios_creados += 1")
        
        nuevo_contenido = partes[0] + codigo_campos_fijo + resto[1]
        nuevo_contenido = nuevo_contenido.replace("\\n", "\n")
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡views.py actualizado con éxito! Los campos de Apellido y Usuario ahora se procesarán de forma independiente.")
    else:
        print("❌ No se localizó el bloque dinámico base en views.py. Verifica si ya fue modificado.")
else:
    print("❌ No se encontró el archivo tikects_app/views.py")
