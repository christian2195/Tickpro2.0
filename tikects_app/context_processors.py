from .models import Notificaciones, Agentes

def agregar_notificaciones(request):
    notificaciones_pendientes = []
    
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'agente'):
                agente_actual = request.user.agente
            else:
                agente_actual = Agentes.objects.filter(usuario=request.user).first()
            
            if agente_actual:
                notificaciones_pendientes = Notificaciones.objects.filter(
                    agente=agente_actual, 
                    leida=False
                ).order_by('-id')[:5]
        except Exception as e:
            print(f"Error en context_processor de notificaciones: {e}")
            notificaciones_pendientes = []
            
    return {
        'notificaciones': notificaciones_pendientes,
        'notificaciones_globales': notificaciones_pendientes
    }