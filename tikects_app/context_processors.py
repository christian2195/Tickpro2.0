from .models import ConfiguracionApariencia

def apariencia_global(request):
    try:
        # Obtenemos la configuración (el ID 1 siempre será nuestro registro único)
        config, created = ConfiguracionApariencia.objects.get_or_create(id=1)
        return {'apariencia': config}
    except Exception:
        # Prevención de errores si la base de datos aún no se ha migrado
        return {'apariencia': None}