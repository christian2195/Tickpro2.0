import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos la forma en que estás importando tus modelos actualmente
    if "from .models import" in contenido:
        # Reemplazamos la línea para asegurarnos de incluir Gerencia de forma explícita
        lineas = contenido.split('\n')
        for i, linea in enumerate(lineas):
            if "from .models import" in linea and "Gerencia" not in linea:
                lineas[i] = linea.replace("from .models import ", "from .models import Gerencia, ")
                print("✅ Se añadió 'Gerencia' a la línea de importación existente.")
                break
        
        nuevo_contenido = '\n'.join(lineas)
    else:
        # Si no se encuentra la línea exacta, la inyectamos al principio del archivo
        nuevo_contenido = "from .models import Gerencia\n" + contenido
        print("✅ Se añadió la importación de Gerencia al principio del archivo.")

    with open(ruta_views, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
else:
    print("❌ No se encontró el archivo tikects_app/views.py")
