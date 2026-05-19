import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Bloque de código mejorado que limpia los títulos y acepta 'Direccion' o 'Gerencia'
    codigo_tolerante = """            df = pd.read_excel(archivo)
            
            # Limpiamos espacios en blanco accidentales en los nombres de las columnas
            df.columns = [str(col).strip() for col in df.columns]
            
            # Si el usuario usó 'Gerencia' en el Excel, la renombramos internamente a 'Direccion' para el bucle
            if 'Gerencia' in df.columns and 'Direccion' not in df.columns:
                df.rename(columns={'Gerencia': 'Direccion'}, inplace=True)
                
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                messages.error(request, "Estructura incorrecta. El Excel debe tener las columnas: Nombre, Apellido, usuario, Clave y Gerencia (o Direccion).")
                return redirect('registrar_usuarios')"""

    # Localizamos el punto exacto de la validación estricta vieja para sustituirlo
    codigo_viejo_estricto = """            df = pd.read_excel(archivo)
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                messages.error(request, "El Excel debe contener las columnas: Nombre, Apellido, usuario, Clave, Direccion")
                return redirect('registrar_usuarios')"""

    if codigo_viejo_estricto in contenido:
        contenido = contenido.replace(codigo_viejo_estricto, codigo_tolerante)
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ ¡views.py actualizado! El validador ahora es flexible con los títulos del Excel.")
    else:
        # Intento de reemplazo secundario si los espacios varían un poco en tu archivo actual
        if "required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']" in contenido:
            print("⚠️ Estructura detectada de forma parcial, aplicando parche alternativo...")
            partes = contenido.split("df = pd.read_excel(archivo)")
            resto = partes[1].split("usuarios_creados = 0")
            
            nuevo_contenido = partes[0] + "df = pd.read_excel(archivo)\\n" + codigo_tolerante + "\\n            usuarios_creados = 0" + resto[1]
            # Limpieza de escapes dobles si el string los duplica
            nuevo_contenido = nuevo_contenido.replace("\\n", "\n")
            
            with open(ruta_views, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            print("✅ ¡views.py actualizado mediante parche alternativo!")
        else:
            print("❌ No se encontró el bloque de validación antiguo exacto en views.py.")
else:
    print("❌ No se encontró el archivo tikects_app/views.py")
