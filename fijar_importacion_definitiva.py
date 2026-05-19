import os

ruta_views = os.path.join('tikects_app', 'views.py')

codigo_definitivo_view = """@superuser_required
@login_required
def registrar_usuarios(request):
    if request.method == 'POST':
        if 'archivo_excel' not in request.FILES:
            messages.error(request, "Por favor, selecciona un archivo Excel.")
            return redirect('registrar_usuarios')
            
        archivo = request.FILES['archivo_excel']
        
        try:
            df = pd.read_excel(archivo)
            df.columns = [str(col).strip() for col in df.columns]
            
            if 'Gerencia' in df.columns and 'Direccion' not in df.columns:
                df.rename(columns={'Gerencia': 'Direccion'}, inplace=True)
                
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                messages.error(request, "Estructura incorrecta. El Excel debe tener las columnas: Nombre, Apellido, usuario, Clave y Gerencia.")
                return redirect('registrar_usuarios')
            
            usuarios_creados = 0
            for _, row in df.iterrows():
                txt_nombre = str(row['Nombre']).strip()
                txt_apellido = str(row['Apellido']).strip()
                username_field = str(row['usuario']).strip()
                txt_clave = str(row['Clave']).strip()
                txt_direccion = str(row['Direccion']).strip()
                
                if txt_nombre.lower() in ['presidencia', 'vicepresidencia', 'negocios', 'comercio', 'logistica', 'seguridad', 'gerencia de', 'prueba', 'transporte']:
                    continue
                if not username_field or username_field.lower() == 'nan':
                    continue

                if not txt_clave or txt_clave.lower() == 'nan':
                    txt_clave = "Emvepro2026*"
                
                if not User.objects.filter(username=username_field).exists():
                    correo_automatico = generar_correo_institucional(txt_nombre, txt_apellido)
                    
                    user = User.objects.create_user(
                        username=username_field,
                        password=txt_clave,
                        email=correo_automatico,
                        first_name=txt_nombre,
                        last_name=txt_apellido
                    )
                    
                    gerencia_obj, _ = Gerencia.objects.get_or_create(
                        nombre=txt_direccion,
                        defaults={'descripcion': f'Gerencia de {txt_direccion}'}
                    )
                    
                    nombre_completo = f"{txt_nombre} {txt_apellido}"
                    
                    import inspect
                    campos_reales = [f.name for f in Cliente._meta.get_fields()]
                    
                    campos_posibles = {
                        'nombre': nombre_completo,
                        'primer_nombre': txt_nombre,
                        'primer_apellido': txt_apellido,
                        'apellido': txt_apellido,
                        'nombre_usuario': username_field,
                        'correo': correo_automatico,
                        'email': correo_automatico,
                        'telefono': '000-000-0000',
                        'gerencia': gerencia_obj,
                        'usuario': user,
                    }
                    
                    argumentos_validos = {k: v for k, v in campos_posibles.items() if k in campos_reales}
                    
                    if 'rif' in campos_reales:
                        argumentos_validos['rif'] = f"V-{user.id:08d}"
                    elif 'cedula' in campos_reales:
                        argumentos_validos['cedula'] = f"{user.id:08d}"
                        
                    Cliente.objects.create(**argumentos_validos)
                    usuarios_creados += 1
            
            messages.success(request, f"¡Carga masiva completada! Se registraron {usuarios_creados} usuarios limpios.")
            return redirect('ver_cliente')
            
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
            
    return render(request, 'registrar_usuarios.html')"""

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Separamos usando un string plano de una sola línea (adiós IndentationError)
    partes = contenido.split("def registrar_usuarios(request):")
    
    # El decorador viejo quedó al final de partes[0], lo removemos para meter el bloque nuevo limpio
    partes_izq = partes[0].split("@superuser_required")
    if len(partes_izq) > 1:
        inicio_archivo = "@superuser_required".join(partes_izq[:-1])
    else:
        inicio_archivo = partes[0]

    # Separamos el código de la función de abajo
    resto_codigo = partes[1].split("def registrar_tickets_excel(request):")
    
    # Armamos la estructura final pegada al ras izquierdo de la terminal
    nuevo_contenido = inicio_archivo + codigo_definitivo_view + "\n\n@superuser_required\n@login_required\ndef registrar_tickets_excel(request):" + resto_codigo[1]
    
    with open(ruta_views, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    print("✅ ¡views.py reestructurado con éxito sin problemas de sangría!")
else:
    print("❌ No se encontró el archivo views.py")
