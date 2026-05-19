import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Ubicamos la función que da problemas para reemplazarla por completo
    if "def registrar_usuarios(request):" in contenido:
        partes = contenido.split("@superuser_required\n@login_required\ndef registrar_usuarios(request):")
        if len(partes) < 2:
            partes = contenido.split("def registrar_usuarios(request):")
            
        resto_codigo = partes[1].split("def registrar_tickets_excel(request):")
        
        codigo_corregido = """
@superuser_required
@login_required
def registrar_usuarios(request):
    ruta = os.path.join(settings.BASE_DIR, 'usuarios_nuevos.xlsx')
    error = None
    if request.method == 'POST':
        try:
            df = pd.read_excel(ruta)
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                raise ValueError("Columnas incorrectas en el Excel. Se requiere: Nombre, Apellido, usuario, Clave, Direccion")
            
            for _, row in df.iterrows():
                if not User.objects.filter(username=row['usuario']).exists():
                    correo_automatico = generar_correo_institucional(row['Nombre'], row['Apellido'])
                    
                    user = User.objects.create_user(
                        username=row['usuario'],
                        password=row['Clave'],
                        email=correo_automatico,
                        first_name=row['Nombre'],
                        last_name=row['Apellido']
                    )
                    
                    nombre_gerencia = str(row['Direccion']).strip()
                    gerencia_obj, _ = Gerencia.objects.get_or_create(
                        nombre=nombre_gerencia,
                        defaults={'descripcion': f'Gerencia de {nombre_gerencia}'}
                    )
                    
                    nombre_completo = f"{row['Nombre']} {row['Apellido']}"
                    rif_temporal = f"V-{user.id:08d}"
                    
                    Cliente.objects.create(
                        nombre=nombre_completo,
                        rif=rif_temporal,
                        telefono='000-000-0000',
                        correo=correo_automatico,
                        gerencia=gerencia_obj
                    )
            return redirect('ver_cliente')
        except Exception as e:
            error = str(e)
    return render(request, 'registrar_usuarios.html', {'error': error})
"""
        nuevo_contenido = partes[0] + codigo_corregido + "\\n\\n@superuser_required\\n@login_required\\ndef registrar_tickets_excel(request):" + resto_codigo[1]
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡views.py corregido con los campos reales del modelo Cliente!")
    else:
        print("❌ No se encontró la función registrar_usuarios.")
else:
    print("❌ No se encontró el archivo views.py")
