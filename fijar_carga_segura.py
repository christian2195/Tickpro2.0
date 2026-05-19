import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Vamos a inyectar una lógica de creación ultra segura que inspecciona los campos del modelo Cliente en caliente
    codigo_seguro = """                    # Creamos el perfil de Cliente adaptándonos dinámicamente a los campos reales del modelo
                    nombre_completo = f"{row['Nombre']} {row['Apellido']}"
                    
                    # Diccionario con todos los campos posibles que han existido en tus versiones
                    campos_posibles = {
                        'nombre': nombre_completo,
                        'correo': correo_automatico,
                        'email': correo_automatico,
                        'telefono': '000-000-0000',
                        'gerencia': gerencia_obj,
                        'direccion': row['Direccion'],
                        'usuario': user,
                    }
                    
                    # Filtramos los campos dejando SOLO los que el modelo Cliente realmente tiene definidos
                    import inspect
                    campos_reales = [f.name for f in Cliente._meta.get_fields()]
                    
                    argumentos_validos = {
                        k: v for k, v in campos_posibles.items() 
                        if k in campos_reales
                    }
                    
                    # Si tu modelo exige un RIF o cédula pero no vino en el diccionario, lo añadimos si el campo existe
                    if 'rif' in campos_reales:
                        argumentos_validos['rif'] = f"V-{user.id:08d}"
                    elif 'cedula' in campos_reales:
                        argumentos_validos['cedula'] = f"{user.id:08d}"
                        
                    Cliente.objects.create(**argumentos_validos)
                    usuarios_creados += 1"""

    # Localizamos el bloque de creación viejo que intentaba meter el 'rif' a la fuerza
    bloque_viejo_rif = """                    nombre_completo = f"{row['Nombre']} {row['Apellido']}"
                    rif_temporal = f"V-{user.id:08d}"
                    
                    Cliente.objects.create(
                        nombre=nombre_completo,
                        rif=rif_temporal,
                        telefono='000-000-0000',
                        correo=correo_automatico,
                        gerencia=gerencia_obj
                    )
                    usuarios_creados += 1"""

    if bloque_viejo_rif in contenido:
        contenido = contenido.replace(bloque_viejo_rif, codigo_seguro)
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ ¡views.py actualizado con el inyector de campos dinámico y seguro!")
    else:
        # Intento de parche por si los espacios cambiaron un poco
        if "rif_temporal =" in contenido:
            print("⚠️ Estructura detectada parcialmente, aplicando reemplazo quirúrgico...")
            # Buscaremos reemplazar desde el nombre completo hasta la creación del objeto
            partes = contenido.split("nombre_completo = f\"{row['Nombre']} {row['Apellido']}\"")
            resto = partes[1].split("usuarios_creados += 1")
            
            nuevo_contenido = partes[0] + codigo_seguro + resto[1]
            # Limpiamos posibles saltos duplicados
            nuevo_contenido = nuevo_contenido.replace("\\n", "\n")
            
            with open(ruta_views, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            print("✅ ¡views.py actualizado mediante parche dinámico alternativo!")
        else:
            print("❌ No se encontró la lógica de asignación del cliente con RIF en views.py.")
else:
    print("❌ No se encontró el archivo tikects_app/views.py")
