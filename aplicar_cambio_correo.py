import os

ruta_views = os.path.join('tikects_app', 'views.py')

# Código nuevo que va a reemplazar la lógica vieja de registro masivo
codigo_nuevo = """
import unicodedata

def generar_correo_institucional(first_name, last_name):
    \"\"\"Limpia los nombres y genera el correo emvepro.gob.ve automáticamente\"\"\"
    nombre = str(first_name).strip().split()[0].lower()
    apellido = str(last_name).strip().split()[0].lower()
    
    # Eliminar acentos y tildes
    nombre = "".join(c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn')
    apellido = "".join(c for c in unicodedata.normalize('NFD', apellido) if unicodedata.category(c) != 'Mn')
    
    # Reemplazar la ñ
    nombre = nombre.replace('ñ', 'n')
    apellido = apellido.replace('ñ', 'n')
    
    return f"{nombre}.{apellido}@emvepro.gob.ve"

@superuser_required
@login_required
def registrar_usuarios(request):
    ruta = os.path.join(settings.BASE_DIR, 'usuarios_nuevos.xlsx')
    error = None
    if request.method == 'POST':
        try:
            df = pd.read_excel(ruta)
            # Ya no se exige la columna 'Correo' de forma obligatoria
            required = ['Nombre', 'Apellido', 'usuario', 'Clave', 'Direccion']
            if not all(col in df.columns for col in required):
                raise ValueError("Columnas incorrectas en el Excel. Se requiere: Nombre, Apellido, usuario, Clave, Direccion")
            
            for _, row in df.iterrows():
                if not User.objects.filter(username=row['usuario']).exists():
                    # Generamos el correo institucional de forma automática
                    correo_automatico = generar_correo_institucional(row['Nombre'], row['Apellido'])
                    
                    user = User.objects.create_user(
                        username=row['usuario'],
                        password=row['Clave'],
                        email=correo_automatico,
                        first_name=row['Nombre'],
                        last_name=row['Apellido']
                    )
                    Cliente.objects.create(
                        nombre=row['Nombre'],
                        apellido=row['Apellido'],
                        nombre_usuario=row['usuario'],
                        email=correo_automatico,
                        telefono='000-000-0000',
                        direccion=row['Direccion'],
                        usuario=user
                    )
            return redirect('ver_cliente')
        except Exception as e:
            error = str(e)
    return render(request, 'registrar_usuarios.html', {'error': error})
"""

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos dónde empieza la función vieja para cortarla y reemplazarla
    if "def registrar_usuarios(request):" in contenido:
        # Dividimos el archivo justo antes de la función vieja
        partes = contenido.split("@superuser_required\n@login_required\ndef registrar_usuarios(request):")
        
        if len(partes) < 2:
            partes = contenido.split("def registrar_usuarios(request):")
            
        # Buscamos la siguiente función principal para no borrar código de más
        # En este caso, la función que le sigue abajo es 'registrar_tickets_excel'
        resto_codigo = partes[1].split("def registrar_tickets_excel(request):")
        
        # Armamos el nuevo archivo uniendo la parte inicial, el bloque nuevo y el resto de las vistas
        nuevo_contenido = partes[0] + codigo_nuevo + "\n\n@superuser_required\n@login_required\ndef registrar_tickets_excel(request):" + resto_codigo[1]
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡views.py actualizado con éxito para la generación automática de correos!")
    else:
        print("❌ No se encontró la función registrar_usuarios en views.py")
else:
    print("❌ No se pudo encontrar el archivo tikects_app/views.py")
