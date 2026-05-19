import os

ruta_models = os.path.join('tikects_app', 'models.py')
ruta_views = os.path.join('tikects_app', 'views.py')

# 1. Corregir el archivo models.py si se guardó en plural
if os.path.exists(ruta_models):
    with open(ruta_models, 'r', encoding='utf-8') as f:
        contenido_models = f.read()
    
    # Cambiamos la declaración de la clase si quedó como 'class Gerencias'
    if "class Gerencias(models.Model):" in contenido_models:
        contenido_models = contenido_models.replace("class Gerencias(models.Model):", "class Gerencia(models.Model):")
        with open(ruta_models, 'w', encoding='utf-8') as f:
            f.write(contenido_models)
        print("✅ Clase corregida a 'Gerencia' en models.py")

# 2. Asegurar la importación limpia en views.py
if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido_views = f.read()
    
    # Reemplazamos cualquier variante corrupta de esa línea específica
    if "from .models import Gerencia, Cliente, Tickets" in contenido_views:
        # Ya está bien estructurada
        pass
    elif "from .models import Gerencias, Cliente, Tickets" in contenido_views:
        contenido_views = contenido_views.replace("from .models import Gerencias,", "from .models import Gerencia,")
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(contenido_views)
        print("✅ Importación actualizada a 'Gerencia' en views.py")
