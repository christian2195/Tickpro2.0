import os

ruta_models = os.path.join('tikects_app', 'models.py')

if os.path.exists(ruta_models):
    with open(ruta_models, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos la línea de la relación que se quedó en plural
    linea_vieja = "gerencia = models.ForeignKey(Gerencias,"
    linea_nueva = "gerencia = models.ForeignKey(Gerencia,"

    if linea_vieja in contenido:
        contenido = contenido.replace(linea_vieja, linea_nueva)
        with open(ruta_models, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ ¡Relación ForeignKey corregida a 'Gerencia' en models.py!")
    else:
        # Intento alternativo por si varía el espaciado
        if "ForeignKey(Gerencias" in contenido:
            contenido = contenido.replace("ForeignKey(Gerencias", "ForeignKey(Gerencia")
            with open(ruta_models, 'w', encoding='utf-8') as f:
                f.write(contenido)
            print("✅ ¡Relación ForeignKey corregida mediante parche alternativo!")
        else:
            print("❌ No se encontró la línea ForeignKey con 'Gerencias' (puede que ya esté modificada).")
else:
    print("❌ No se encontró el archivo tikects_app/models.py")
