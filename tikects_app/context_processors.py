from .models import Notificaciones

def agregar_notificaciones(request):
    notificaciones = Notificaciones.objects.all()
    return {
        'notificaciones': notificaciones
    }
