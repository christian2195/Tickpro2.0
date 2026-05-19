import os

# Diccionario de reemplazos (ordenado de plural a singular para no sobreescribir mal)
reemplazos = {
    'Direcciones': 'Gerencias',
    'direcciones': 'gerencias',
    'DIRECCIONES': 'GERENCIAS',
    'Dirección': 'Gerencia',
    'dirección': 'gerencia',
    'Direccion': 'Gerencia',
    'direccion': 'gerencia',
    'DIRECCION': 'GERENCIA',
}

def reemplazar_en_archivo(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return
    
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    
    nuevo_contenido = contenido
    for viejo, nuevo in reemplazos.items():
        nuevo_contenido = nuevo_contenido.replace(viejo, nuevo)
        
    if nuevo_contenido != contenido:
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(nuevo_contenido)
        print(f"✅ Texto actualizado en: {ruta_archivo}")

# 1. Archivos Python principales a modificar
app_dir = 'tikects_app'
archivos_python = [
    os.path.join(app_dir, 'models.py'),
    os.path.join(app_dir, 'views.py'),
    os.path.join(app_dir, 'urls.py'),
    os.path.join(app_dir, 'admin.py'),
]

print("Iniciando reemplazo de texto...")
for archivo in archivos_python:
    reemplazar_en_archivo(archivo)

# 2. Modificar texto en Plantillas (Templates) y renombrar archivos
templates_dir = os.path.join(app_dir, 'templates')
if os.path.exists(templates_dir):
    for filename in os.listdir(templates_dir):
        if filename.endswith('.html'):
            ruta_completa = os.path.join(templates_dir, filename)
            reemplazar_en_archivo(ruta_completa)
            
    # Renombrar los archivos físicos que tengan "direccion" en el nombre
    for filename in os.listdir(templates_dir):
        if 'direccion' in filename.lower():
            nuevo_nombre = filename
            for viejo, nuevo in reemplazos.items():
                nuevo_nombre = nuevo_nombre.replace(viejo, nuevo)
            
            ruta_vieja = os.path.join(templates_dir, filename)
            ruta_nueva = os.path.join(templates_dir, nuevo_nombre)
            os.rename(ruta_vieja, ruta_nueva)
            print(f"🔄 Archivo renombrado: {filename} ➔ {nuevo_nombre}")

print("\n🚀 ¡Script finalizado con éxito! Todos los cambios aplicados para EMVEPRO.")
