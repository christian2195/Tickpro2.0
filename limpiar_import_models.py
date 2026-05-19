import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Buscaremos la sección rota de la importación y la reescribiremos limpia
    nueva_cabecera_modelos = "from .models import Gerencia, Cliente, Tickets\n"
    
    lineas_filtradas = []
    saltarse = False
    importacion_reemplazada = False

    for linea in lineas:
        # Detectamos el inicio del bloque roto
        if "from .models import" in linea and not importacion_reemplazada:
            lineas_filtradas.append(nueva_cabecera_modelos)
            importacion_reemplazada = True
            # Si la línea original abría un paréntesis multilínea, nos saltamos las líneas hasta que cierre
            if "(" in linea and ")" not in linea:
                saltarse = True
            continue
            
        if saltarse:
            if ")" in linea:
                saltarse = False
            continue
            
        lineas_filtradas.append(linea)

    with open(ruta_views, 'w', encoding='utf-8') as f:
        f.writelines(lineas_filtradas)
        
    print("✅ ¡Bloque de importación en views.py saneado con éxito!")
else:
    print("❌ No se encontró el archivo views.py")
