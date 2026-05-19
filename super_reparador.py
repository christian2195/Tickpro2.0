import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Vamos a buscar la función entera 'cerrar_tikect' para reconstruirla limpia y perfecta
    # Identificamos el inicio de la función
    if "def cerrar_tikect(request, tikect_id):" in contenido:
        # Dividimos el archivo justo donde empieza la función cerrar_tikect
        partes = contenido.split("@login_required\ndef cerrar_tikect(request, tikect_id):")
        if len(partes) < 2:
            partes = contenido.split("def cerrar_tikect(request, tikect_id):")
        
        # Conseguimos el inicio del resto del código dividiendo en la siguiente función del archivo ('reasignar_tikect')
        resto_codigo = partes[1].split("def reasignar_tikect(request, tikect_id):")
        
        # Definimos la función cerrar_tikect reestructurada con triple comilla limpia
        funcion_limpia = """@login_required
def cerrar_tikect(request, tikect_id):
    tikect = get_object_or_404(Tickets, id=tikect_id)
    if request.method == 'POST':
        descripcion_solucion = request.POST.get('descripcion_solucion')
        tikect.estado = 'cerrado'
        tikect.fecha_cierre = timezone.now()
        tikect.descripcion_solucion = descripcion_solucion
        tikect.cerrado_por_agente = request.user
        tikect.save()
        
        # Notificación por Correo Automatizada
        if tikect.usuario and tikect.usuario.email:
            asunto = f"Ticket Cerrado: #{tikect.id} - {tikect.titulo}"
            mensaje = f\"\"\"Hola {tikect.usuario.first_name},

Tu ticket ha sido marcado como CERRADO.
Solución aplicada: {descripcion_solucion}

Gracias por contactarnos.
\"\"\"
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    asunto,
                    mensaje,
                    settings.DEFAULT_FROM_EMAIL,
                    [tikect.usuario.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error enviando correo: {e}")

        if hasattr(request.user, 'agente'):
            return redirect('ver_tikects_asignados_agentes')
        else:
            return redirect('ver_tikects')
    return redirect('detalle_tikect', tikect_id=tikect.id)


@login_required
"""
        
        # Ensamblamos todo el archivo views.py sin caracteres corruptos ni strings huérfanos
        nuevo_contenido = partes[0] + funcion_limpia + "def reasignar_tikect(request, tikect_id):" + resto_codigo[1]
        
        with open(ruta_views, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print("✅ ¡Sintaxis de views.py saneada y reconstruida al 100%!")
    else:
        print("❌ No se detectó el inicio de la función cerrar_tikect.")
else:
    print("❌ No se encontró el archivo views.py")
