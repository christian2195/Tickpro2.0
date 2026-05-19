import os

ruta_views = os.path.join('tikects_app', 'views.py')

funcion_exportar = """
@superuser_required
@login_required
def exportar_usuarios_excel(request):
    \"\"\"Genera un archivo Excel con la lista de clientes actual en la BD\"\"\"
    clientes = Cliente.objects.all().order_by('nombre')
    datos = []
    for c in clientes:
        datos.append({
            'Nombre Completo': c.nombre,
            'RIF': c.rif if hasattr(c, 'rif') else 'N/A',
            'Nombre de Usuario': c.usuario.username if c.usuario else 'N/A',
            'Correo Institucional': c.correo if hasattr(c, 'correo') else (c.email if hasattr(c, 'email') else 'N/A'),
            'Teléfono': c.telefono if hasattr(c, 'telefono') else 'N/A',
            'Gerencia': c.gerencia.nombre if (hasattr(c, 'gerencia') and c.gerencia) else 'Sin Asignar'
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

    # Buscamos el final de la vista de registro para acoplar la de exportación
    punto_de_anclaje = "return render(request, 'registrar_usuarios.html')"
    
    if punto_de_anclaje in contenido and "def exportar_usuarios_excel" not in contenido:
        partes = contenido.split(punto_de_anclaje)
        # Inyectamos la función intermedia respetando el return de la primera
        nuevo_contenido = partes[0] + punto_de_anclaje + "\n\n" + funcion_exportar + partes[1]
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡Función exportar_usuarios_excel restaurada con éxito en views.py!")
    else:
        print("⚠️ La función ya existe o no se encontró el punto de anclaje exacto.")
else:
    print("❌ No se encontró el archivo views.py")
