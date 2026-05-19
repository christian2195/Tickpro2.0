import os

ruta_views = os.path.join('tikects_app', 'views.py')

codigo_web_nuevo = """
import io
import pandas as pd
from django.http import HttpResponse

@superuser_required
@login_required
def registrar_usuarios(request):
    if request.method == 'POST':
        if 'archivo_excel' not in request.FILES:
            messages.error(request, "Por favor, selecciona un archivo Excel.")
            return redirect('registrar_usuarios')
            
        archivo = request.FILES['archivo_excel']
        
        try:
            df = pd.read_excel(archivo)
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                messages.error(request, "El Excel debe contener las columnas: Nombre, Apellido, usuario, Clave, Direccion")
                return redirect('registrar_usuarios')
            
            usuarios_creados = 0
            for _, row in df.iterrows():
                username_field = str(row['usuario']).strip()
                
                if not User.objects.filter(username=username_field).exists():
                    correo_automatico = generar_correo_institucional(row['Nombre'], row['Apellido'])
                    
                    user = User.objects.create_user(
                        username=username_field,
                        password=str(row['Clave']),
                        email=correo_automatico,
                        first_name=str(row['Nombre']).strip(),
                        last_name=str(row['Apellido']).strip()
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
                    usuarios_creados += 1
            
            messages.success(request, f"¡Carga masiva completada! Se registraron {usuarios_creados} usuarios en EMVEPRO.")
            return redirect('ver_cliente')
            
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
            
    return render(request, 'registrar_usuarios.html')


@superuser_required
@login_required
def exportar_usuarios_excel(request):
    \"\"\"Genera un archivo Excel con la lista de clientes actual en la BD\"\"\"
    clientes = Cliente.objects.all().order_by('nombre')
    datos = []
    for c in clientes:
        datos.append({
            'Nombre Completo': c.nombre,
            'RIF': c.rif,
            'Nombre de Usuario': c.usuario.username if c.usuario else 'N/A',
            'Correo Institucional': c.correo,
            'Teléfono': c.telefono,
            'Gerencia': c.gerencia.nombre if c.gerencia else 'Sin Asignar'
        })
    
    df = pd.DataFrame(datos)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes EMVEPRO')
    
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="clientes_emvepro_exportados.xlsx"'
    return response
"""

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    if "def registrar_usuarios(request):" in contenido:
        # Dividimos el archivo justo antes de la función que vamos a suplantar
        partes = contenido.split("@superuser_required\n@login_required\ndef registrar_usuarios(request):")
        if len(partes) < 2:
            partes = contenido.split("def registrar_usuarios(request):")
            
        # Cortamos el resto del archivo conservando lo que viene abajo (registrar_tickets_excel)
        resto_codigo = partes[1].split("def registrar_tickets_excel(request):")
        
        # Unimos las piezas con la nueva funcionalidad web limpia
        nuevo_contenido = partes[0] + codigo_web_nuevo + "\n\n@superuser_required\n@login_required\ndef registrar_tickets_excel(request):" + resto_codigo[1]
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡views.py actualizado! Lógica de importación web y exportación a Excel inyectada.")
    else:
        print("❌ No se encontró la función registrar_usuarios vieja en views.py.")
else:
    print("❌ No se encontró el archivo views.py")
