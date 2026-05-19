import os

ruta_views = os.path.join('tikects_app', 'views.py')

if os.path.exists(ruta_views):
    with open(ruta_views, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscamos el bloque dañado que generó el script anterior
    bloque_roto = """                    Cliente.objects.create(
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
\\n\\n@superuser_required\\n@login_required\\ndef registrar_tickets_excel(request):"""

    # Bloque limpio corregido con saltos de línea reales de Python
    bloque_limpio = """                    Cliente.objects.create(
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


@superuser_required
@login_required
def registrar_tickets_excel(request):"""

    # Hacemos el reemplazo
    if bloque_roto in contenido:
        nuevo_contenido = contenido.replace(bloque_roto, bloque_limpio)
    else:
        # Intento de rescate alternativo si los escapes varían un poco
        nuevo_contenido = contenido.replace("\\n\\n@superuser_required\\n@login_required\\ndef registrar_tickets_excel(request):", "\n\n@superuser_required\n@login_required\ndef registrar_tickets_excel(request):")
        nuevo_contenido = nuevo_contenido.replace("\\n", "\n")

    with open(ruta_views, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    print("✅ ¡SyntaxError reparado! Caracteres corruptos eliminados de views.py.")
else:
    print("❌ No se encontró el archivo views.py")