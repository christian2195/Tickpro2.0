from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Prefetch, Count, F, Avg
from django.db.models.functions import TruncMonth, TruncWeek
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

# ============================================
# MODELOS
# ============================================
from .models import (
    Gerencia, Cliente, Tickets, 
    Agentes, Notificaciones, ReasignacionTikects, 
    Tickets_Servicios, Tickets_Respuestas_Automaticas,
    Grupos_Agentes, Agentes_Por_Grupos, Grupos_Clientes, 
    AsignacionTikects, AgenteGenerico
)

# ============================================
# DECORADORES PERSONALIZADOS
# ============================================

def superuser_required(view_func):
    """Verifica que el usuario sea superusuario."""
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser,
        login_url='pagina_principal'
    )(view_func)
    return decorated_view_func

def agente_or_superuser_required(view_func):
    """Verifica que el usuario sea agente o superusuario."""
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser or hasattr(user, 'agente'),
        login_url='login'
    )(view_func)
    return decorated_view_func

# ============================================
# AUTENTICACIÓN
# ============================================

def inicio(request):
    if request.method == 'GET':
        return render(request, 'inicio de sesion/inicio_sesion.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('clave')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('pagina_principal')
        else:
            return render(request, 'inicio de sesion/inicio_sesion.html', {
                'error': 'Error: usuario o contraseña incorrecta'
            })

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('/')

# ============================================
# PÁGINA PRINCIPAL
# ============================================

@login_required
def pagina_principal(request):
    user = request.user
    now = datetime.now()
    
    agente = None
    notificaciones = []
    ultimos_tickets = []
    context = {'now': now}

    try:
        if hasattr(user, 'agente'):
            agente = user.agente
        else:
            agente = Agentes.objects.filter(usuario=user).first()
    except Exception as e:
        print(f"Error al verificar agente: {e}")
        agente = None
        
    context['agente'] = agente

    if user.is_superuser or agente:
        if agente:
            notificaciones = Notificaciones.objects.filter(agente=agente, leida=False)[:5]
            
        if user.is_superuser:
            ultimos_tickets = Tickets.objects.all().order_by('-fecha_creacion')[:5]
        else:
            tickets_creados = Tickets.objects.filter(usuario=user)
            tickets_reasignados = Tickets.objects.filter(
                id__in=ReasignacionTikects.objects.filter(agente_nuevo=agente).values_list('tikect_id', flat=True)
            )
            ultimos_tickets = (tickets_creados | tickets_reasignados).distinct().order_by('-fecha_creacion')[:5]

        context.update({
            'notificaciones': notificaciones,
            'total_tickets': Tickets.objects.count(),
            'tickets_abiertos': Tickets.objects.exclude(estado='cerrado').count(),
            'tickets_cerrados': Tickets.objects.filter(estado__iexact='cerrado').count(),
            'total_agentes': Agentes.objects.count(),
        })
    else:
        ultimos_tickets = Tickets.objects.filter(usuario=user).order_by('-fecha_creacion')[:5]
        context.update({
            'total_mis_tickets': Tickets.objects.filter(usuario=user).count(),
            'mis_tickets_abiertos': Tickets.objects.filter(usuario=user).exclude(estado='cerrado').count(),
            'mis_tickets_cerrados': Tickets.objects.filter(usuario=user, estado='cerrado').count(),
        })

    context['ultimos_tickets'] = ultimos_tickets
    return render(request, 'inicio de sesion/pagina_principal.html', context)

# ============================================
# CONFIGURACIÓN
# ============================================

@superuser_required
@login_required
def configuracion(request):
    return render(request, 'configuracion/configuracion.html')

# ============================================
# SERVICIOS Y RESPUESTAS AUTOMÁTICAS
# ============================================

@superuser_required
@login_required
def tikects_servicios(request):
    servicios = Tickets_Servicios.objects.all()
    return render(request, 'tickets/gestion_servicios.html', {'servicios': servicios})

@login_required
def tikects_respuestas_automaticas(request):
    respuestas_automaticas = Tickets_Respuestas_Automaticas.objects.all()
    return render(request, 'tickets/gestion_respuestas.html', {
        'respuestas_automaticas': respuestas_automaticas
    })

@superuser_required
@login_required
def tikects_servicios_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre and descripcion:
            Tickets_Servicios.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, f'Servicio "{nombre}" creado con éxito.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
        return redirect('tikects_servicios')
    return redirect('tikects_servicios')

@superuser_required
@login_required
def tikects_respuestas_automaticas_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('respuesta', '').strip()
        if nombre:
            Tickets_Respuestas_Automaticas.objects.create(nombre=nombre)
            messages.success(request, 'Respuesta automática creada con éxito.')
        else:
            messages.error(request, 'La respuesta es obligatoria.')
        return redirect('tikects_respuestas_automaticas')
    return redirect('tikects_respuestas_automaticas')

@superuser_required
@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Tickets_Servicios, id=servicio_id)
    if request.method == 'POST':
        nombre = servicio.nombre
        servicio.delete()
        messages.success(request, f'Servicio "{nombre}" eliminado.')
    return redirect('tikects_servicios')

@superuser_required
@login_required
def eliminar_respuesta_automatica(request, respuesta_id):
    respuesta = get_object_or_404(Tickets_Respuestas_Automaticas, id=respuesta_id)
    if request.method == 'POST':
        nombre = respuesta.nombre[:50]
        respuesta.delete()
        messages.success(request, f'Respuesta automática "{nombre}..." eliminada.')
    return redirect('tikects_respuestas_automaticas')

@superuser_required
@login_required
def editar_servicios(request, servicio_id):
    servicio = get_object_or_404(Tickets_Servicios, id=servicio_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre and descripcion:
            servicio.nombre = nombre
            servicio.descripcion = descripcion
            servicio.save()
            messages.success(request, f'Servicio "{nombre}" actualizado.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
        return redirect('tikects_servicios')
    return redirect('tikects_servicios')

# ============================================
# CLIENTES (VERSION UNIFICADA CON MODALES)
# ============================================

@superuser_required
@login_required
def clientes(request):
    clientes_list = Cliente.objects.all().order_by('nombre')
    paginator = Paginator(clientes_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'usuarios/gestion_clientes.html', {'page_obj': page_obj})

@superuser_required
@login_required
def crear_clientes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip() or None
        telefono = request.POST.get('telefono', '').strip() or None
        password = request.POST.get('password', '').strip()
        gerencia_input = request.POST.get('gerencia', '').strip()

        if not nombre or not apellido or not username or not password or not gerencia_input:
            messages.error(request, "Todos los campos marcados como obligatorios deben ser completados.")
            return redirect('ver_cliente')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"El nombre de usuario '{username}' ya se encuentra registrado.")
            return redirect('ver_cliente')

        try:
            if gerencia_input.isdigit():
                gerencia_obj = get_object_or_404(Gerencia, id=int(gerencia_input))
            else:
                gerencia_obj, _ = Gerencia.objects.get_or_create(
                    nombre=gerencia_input,
                    defaults={'descripcion': f'Gerencia de {gerencia_input}'}
                )

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=nombre,
                last_name=apellido,
                email=email
            )
            
            Cliente.objects.create(
                nombre=f"{nombre} {apellido}",
                correo=email,
                telefono=telefono,
                gerencia=gerencia_obj,
                usuario=user
            )
            
            messages.success(request, f"Cliente '{nombre} {apellido}' registrado con éxito.")
            return redirect('ver_cliente')
            
        except Exception as e:
            messages.error(request, f"Error de base de datos al registrar: {str(e)}")
            return redirect('ver_cliente')
            
    return redirect('ver_cliente')

@superuser_required
@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip() or None
        telefono = request.POST.get('telefono', '').strip() or None
        gerencia_input = request.POST.get('gerencia', '').strip()
        password = request.POST.get('password', '').strip()

        if not nombre or not apellido or not username or not gerencia_input:
            messages.error(request, "Nombre, apellido, usuario y gerencia son obligatorios.")
            return redirect('ver_cliente')

        try:
            user = cliente.usuario
            user.username = username
            user.first_name = nombre
            user.last_name = apellido
            user.email = email
            if password:
                user.set_password(password)
            user.save()

            cliente.nombre = f"{nombre} {apellido}"
            cliente.correo = email
            cliente.telefono = telefono
            cliente.gerencia = gerencia_input
            cliente.save()

            messages.success(request, f"Cliente '{nombre} {apellido}' actualizado con éxito.")
        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")
        
        return redirect('ver_cliente')
    
    return redirect('ver_cliente')

@superuser_required
@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        try:
            nombre = cliente.nombre
            cliente.delete()
            messages.success(request, f"Cliente '{nombre}' eliminado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar cliente: {str(e)}")
    return redirect('ver_cliente')

# ============================================
# GRUPOS DE CLIENTES (VERSION UNIFICADA)
# ============================================

@superuser_required
@login_required
def usuarios_clientes_grupos(request):
    grupos_clientes = Grupos_Clientes.objects.all()
    return render(request, 'usuarios/gestion_grupos_clientes.html', {'grupos_clientes': grupos_clientes})

@superuser_required
@login_required
def usuarios_clientes_grupos_crear(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre and descripcion:
            Grupos_Clientes.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, 'Grupo de clientes creado con éxito.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    return redirect('usuarios_clientes_grupos')

@superuser_required
@login_required
def editar_grupo_clientes(request, grupo_id):
    grupo = get_object_or_404(Grupos_Clientes, id=grupo_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre and descripcion:
            grupo.nombre = nombre
            grupo.descripcion = descripcion
            grupo.save()
            messages.success(request, 'Grupo actualizado con éxito.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    return redirect('usuarios_clientes_grupos')

@superuser_required
@login_required
def eliminar_grupo_clientes(request, grupo_id):
    grupo = get_object_or_404(Grupos_Clientes, id=grupo_id)
    if request.method == 'POST':
        nombre = grupo.nombre
        grupo.delete()
        messages.success(request, f'Grupo "{nombre}" eliminado.')
    return redirect('usuarios_clientes_grupos')

# ============================================
# AGENTES Y GRUPOS (VERSION UNIFICADA CON MODALES)
# ============================================

@superuser_required
@login_required
def gestion_agentes(request):
    agentes = Agentes.objects.select_related('usuario').all()
    
    if request.method == 'POST':
        agente_id = request.POST.get('agente_id')
        if agente_id:
            return editar_agente(request, agente_id)
        else:
            return crear_agente(request)
    
    return render(request, 'agentes/gestion_agentes.html', {'agentes': agentes})

def crear_agente(request):
    nombre = request.POST.get('first_name', '').strip()
    apellido = request.POST.get('last_name', '').strip()
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    if not all([nombre, apellido, username, email, password]):
        messages.error(request, "Todos los campos son obligatorios.")
        return redirect('gestion_agentes')

    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': nombre, 'last_name': apellido}
        )
        
        if not created:
            user.first_name = nombre
            user.last_name = apellido
            user.email = email
            if password:
                user.set_password(password)
            user.save()
            messages.info(request, f"Usuario {username} actualizado.")
        else:
            user.set_password(password)
            user.save()
            messages.success(request, f"Usuario {username} creado exitosamente.")
        
        agente, created = Agentes.objects.get_or_create(
            usuario=user,
            defaults={
                'nombre_usuario': username,
                'nombre': nombre,
                'apellido': apellido,
                'correo': email,
            }
        )
        
        if not created:
            agente.nombre_usuario = username
            agente.nombre = nombre
            agente.apellido = apellido
            agente.correo = email
            agente.save()
            messages.info(request, f"Perfil de agente para {username} actualizado.")
        else:
            messages.success(request, f"Perfil de agente para {username} creado.")
        
        return redirect('gestion_agentes')
        
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('gestion_agentes')

@superuser_required
@login_required
def editar_agente(request, agente_id):
    agente = get_object_or_404(Agentes, id=agente_id)
    usuario = agente.usuario

    if request.method == 'POST':
        nombre = request.POST.get('first_name', '').strip()
        apellido = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        nueva_password = request.POST.get('password', '').strip()

        if not all([nombre, apellido, username, email]):
            messages.error(request, "Nombre, apellido, usuario y email son obligatorios.")
            return redirect('gestion_agentes')

        try:
            usuario.username = username
            usuario.first_name = nombre
            usuario.last_name = apellido
            usuario.email = email
            if nueva_password:
                usuario.set_password(nueva_password)
            usuario.save()

            agente.nombre_usuario = username
            agente.nombre = nombre
            agente.apellido = apellido
            agente.correo = email
            agente.save()

            messages.success(request, f"Agente '{username}' actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar: {str(e)}")
        
        return redirect('gestion_agentes')

    return redirect('gestion_agentes')

@superuser_required
@login_required
def eliminar_agente(request, agente_id):
    agente = get_object_or_404(Agentes, id=agente_id)
    if request.method == 'POST':
        try:
            nombre_usuario = agente.nombre_usuario
            agente.delete()
            messages.success(request, f"Agente '{nombre_usuario}' eliminado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el agente: {str(e)}")
    return redirect('gestion_agentes')

# ============================================
# GRUPOS DE AGENTES (VERSION UNIFICADA)
# ============================================

@superuser_required
@login_required
def gestion_grupos(request):
    grupos_agentes = Grupos_Agentes.objects.prefetch_related(
        Prefetch('agentes_por_grupos_set', 
                 queryset=Agentes_Por_Grupos.objects.select_related('agente__usuario'))
    ).all()
    agentes = Agentes.objects.select_related('usuario').all()
    
    if request.method == 'POST':
        grupo_id = request.POST.get('grupo_id')
        if grupo_id:
            grupo = get_object_or_404(Grupos_Agentes, id=grupo_id)
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if nombre and descripcion:
                grupo.nombre = nombre
                grupo.descripcion = descripcion
                grupo.save()
                messages.success(request, 'Grupo actualizado con éxito.')
            else:
                messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('gestion_grupos')
        else:
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if nombre and descripcion:
                Grupos_Agentes.objects.create(nombre=nombre, descripcion=descripcion)
                messages.success(request, 'Grupo creado con éxito.')
            else:
                messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('gestion_grupos')
    
    return render(request, 'agentes/gestion_grupos.html', {
        'grupos_agentes': grupos_agentes,
        'agentes': agentes
    })

@superuser_required
@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupos_Agentes, id=grupo_id)
    if request.method == 'POST':
        nombre = grupo.nombre
        grupo.delete()
        messages.success(request, f"Grupo '{nombre}' eliminado.")
    return redirect('gestion_grupos')

@superuser_required
@login_required
def asignar_agente_grupo(request):
    if request.method == 'POST':
        agente_id = request.POST.get('agente')
        grupo_id = request.POST.get('grupo')
        
        if not agente_id or not grupo_id:
            messages.error(request, "Debe seleccionar un agente y un grupo.")
            return redirect('gestion_grupos')
        
        agente = get_object_or_404(Agentes, id=agente_id)
        grupo = get_object_or_404(Grupos_Agentes, id=grupo_id)
        
        if Agentes_Por_Grupos.objects.filter(agente=agente, grupo=grupo).exists():
            messages.warning(request, f"El agente ya pertenece al grupo {grupo.nombre}.")
        else:
            Agentes_Por_Grupos.objects.create(agente=agente, grupo=grupo)
            messages.success(request, f"Agente asignado al grupo {grupo.nombre}.")
    
    return redirect('gestion_grupos')

@superuser_required
@login_required
def quitar_agente_grupo(request, grupo_agente_id):
    grupo_agente = get_object_or_404(Agentes_Por_Grupos, id=grupo_agente_id)
    if request.method == 'POST':
        usuario = grupo_agente.agente.nombre_usuario
        grupo = grupo_agente.grupo.nombre
        grupo_agente.delete()
        messages.success(request, f"Agente {usuario} removido del grupo {grupo}.")
    return redirect('gestion_grupos')

# ============================================
# AGENTES GENÉRICOS (VERSION UNIFICADA)
# ============================================

@superuser_required
@login_required
def gestion_genericos(request):
    asignaciones = AgenteGenerico.objects.select_related(
        'servicio', 'agente_actual__usuario', 'agente_reasignacion__usuario'
    ).all()
    servicios = Tickets_Servicios.objects.all()
    agentes = Agentes.objects.select_related('usuario').all()
    
    if request.method == 'POST':
        return crear_asignacion_generica(request)
    
    return render(request, 'agentes/gestion_genericos.html', {
        'asignaciones': asignaciones,
        'servicios': servicios,
        'agentes': agentes
    })

@superuser_required
@login_required
def crear_asignacion_generica(request):
    if request.method != 'POST':
        return redirect('gestion_genericos')
    
    servicio_id = request.POST.get('servicio')
    agente_actual_id = request.POST.get('agente_actual')
    tiempo_reasignacion = request.POST.get('tiempo_reasignacion')
    agente_reasignacion_id = request.POST.get('agente_reasignacion')
    
    if not servicio_id or not agente_actual_id:
        messages.error(request, "Debe seleccionar un servicio y un agente actual.")
        return redirect('gestion_genericos')
    
    try:
        servicio = get_object_or_404(Tickets_Servicios, id=servicio_id)
        agente_actual = get_object_or_404(Agentes, id=agente_actual_id)
        agente_reasignacion = get_object_or_404(Agentes, id=agente_reasignacion_id) if agente_reasignacion_id else None
        
        if AgenteGenerico.objects.filter(servicio=servicio).exists():
            messages.warning(request, f"El servicio {servicio.nombre} ya tiene una asignación.")
            return redirect('gestion_genericos')
        
        tiempo = int(tiempo_reasignacion) if tiempo_reasignacion and tiempo_reasignacion.isdigit() else None
        
        AgenteGenerico.objects.create(
            servicio=servicio,
            agente_actual=agente_actual,
            tiempo_reasignacion=tiempo,
            agente_reasignacion=agente_reasignacion
        )
        messages.success(request, f"Asignación genérica creada para {servicio.nombre}.")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('gestion_genericos')

@superuser_required
@login_required
def eliminar_asignacion_generica(request, asignacion_id):
    asignacion = get_object_or_404(AgenteGenerico, id=asignacion_id)
    if request.method == 'POST':
        servicio = asignacion.servicio.nombre
        asignacion.delete()
        messages.success(request, f"Asignación genérica para {servicio} eliminada.")
    return redirect('gestion_genericos')

# ============================================
# PERMISOS (VERSION UNIFICADA)
# ============================================

@superuser_required
@login_required
def gestion_permisos(request):
    agentes = Agentes.objects.select_related('usuario').all()
    grupos = Grupos_Agentes.objects.prefetch_related('agentes_por_grupos_set').all()
    return render(request, 'agentes/gestion_permisos.html', {
        'agentes': agentes,
        'grupos': grupos
    })

# ============================================
# GERENCIAS (VERSION UNIFICADA)
# ============================================

@superuser_required
@login_required
def gestion_gerencias(request):
    gerencias = Gerencia.objects.all()
    
    if request.method == 'POST':
        gerencia_id = request.POST.get('gerencia_id')
        if gerencia_id:
            gerencia = get_object_or_404(Gerencia, id=gerencia_id)
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if nombre and descripcion:
                gerencia.nombre = nombre
                gerencia.descripcion = descripcion
                gerencia.save()
                messages.success(request, 'Gerencia actualizada con éxito.')
            else:
                messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('gestion_gerencias')
        else:
            nombre = request.POST.get('nombre', '').strip()
            descripcion = request.POST.get('descripcion', '').strip()
            if nombre and descripcion:
                Gerencia.objects.create(nombre=nombre, descripcion=descripcion)
                messages.success(request, 'Gerencia creada con éxito.')
            else:
                messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('gestion_gerencias')
    
    return render(request, 'configuracion/gestion_gerencias.html', {'gerencias': gerencias})

@superuser_required
@login_required
def eliminar_gerencia(request, gerencia_id):
    gerencia = get_object_or_404(Gerencia, id=gerencia_id)
    if request.method == 'POST':
        nombre = gerencia.nombre
        gerencia.delete()
        messages.success(request, f'Gerencia "{nombre}" eliminada.')
    return redirect('gestion_gerencias')

# ============================================
# TICKETS - VISTAS PRINCIPALES (UNIFICADAS)
# ============================================

def _get_tickets_base(request, estado=None):
    """Función auxiliar para obtener tickets filtrados por estado"""
    user = request.user
    
    if user.is_superuser:
        queryset = Tickets.objects.all()
    else:
        # Para agentes, mostrar tickets creados por ellos o reasignados
        try:
            agente = Agentes.objects.get(usuario=user)
            tickets_creados = Tickets.objects.filter(usuario=user)
            tickets_reasignados = Tickets.objects.filter(
                id__in=ReasignacionTikects.objects.filter(agente_nuevo=agente).values_list('tikect_id', flat=True)
            )
            queryset = (tickets_creados | tickets_reasignados).distinct()
        except Agentes.DoesNotExist:
            # Para clientes normales, solo sus tickets
            queryset = Tickets.objects.filter(usuario=user)
    
    if estado == 'cerrado':
        queryset = queryset.filter(estado__iexact='cerrado')
    elif estado == 'abierto':
        queryset = queryset.exclude(estado__iexact='cerrado')
    
    return queryset.order_by('-fecha_creacion')

def _get_reasignaciones_dict(tikects):
    """Función auxiliar para obtener diccionario de reasignaciones"""
    reasignaciones_dict = {}
    for r in ReasignacionTikects.objects.all():
        try:
            if r.agente_nuevo:
                reasignaciones_dict[r.ticket_id] = r.agente_nuevo.nombre_usuario
        except:
            pass
    return reasignaciones_dict

@login_required
def ver_tikects(request):
    estado = None
    url_name = request.resolver_match.url_name
    if url_name == 'ver_tikects_cerrados':
        estado = 'cerrado'
    elif url_name == 'ver_tikects_abiertos':
        estado = 'abierto'
    
    tikects = _get_tickets_base(request, estado)
    paginator = Paginator(tikects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    reasignaciones_dict = _get_reasignaciones_dict(tikects)
    
    return render(request, 'tickets/tikects_ver_todos.html', {
        'tikects': page_obj,
        'reasignaciones_dict': reasignaciones_dict
    })

ver_tikects_cerrados = ver_tikects
ver_tikects_abiertos = ver_tikects

# ============================================
# TICKETS - CLIENTES
# ============================================

@login_required
def ver_mis_tikects(request):
    estado = None
    url_name = request.resolver_match.url_name
    if url_name == 'ver_mis_tikects_cerrados':
        estado = 'cerrado'
    elif url_name == 'ver_mis_tikects_abiertos':
        estado = 'abierto'
    
    tikects = Tickets.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    if estado == 'cerrado':
        tikects = tikects.filter(estado='cerrado')
    elif estado == 'abierto':
        tikects = tikects.exclude(estado='cerrado')
    
    paginator = Paginator(tikects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tickets/tikects_vista_lista_cliente.html', {'page_obj': page_obj})

ver_mis_tikects_cerrados = ver_mis_tikects
ver_mis_tikects_abiertos = ver_mis_tikects

# ============================================
# TICKETS - VISTAS PARA AGENTES
# ============================================

@login_required
def ver_tikects_asignados_agentes(request):
    """Vista para agentes o superusuarios: ver tickets asignados"""
    user = request.user
    
    # Si es superusuario, mostrar todos los tickets
    if user.is_superuser:
        tickets_base = Tickets.objects.all().order_by('-fecha_creacion')
        tikects_cerrados = tickets_base.filter(estado__iexact='cerrado').count()
        tikects_abiertos = tickets_base.exclude(estado__iexact='cerrado').count()
        
        url_name = request.resolver_match.url_name
        if url_name == 'ver_tikects_asignados_agentes_cerrados':
            tickets_filtrados = tickets_base.filter(estado__iexact='cerrado')
        elif url_name == 'ver_tikects_asignados_agentes_abiertos':
            tickets_filtrados = tickets_base.exclude(estado__iexact='cerrado')
        else:
            tickets_filtrados = tickets_base
            
        paginator = Paginator(tickets_filtrados, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Crear un set de IDs de tickets reasignados para consulta rápida
        reasignados_ids = set()
        for r in ReasignacionTikects.objects.all():
            try:
                if r.agente_nuevo:
                    reasignados_ids.add(r.ticket_id)
            except:
                pass

        context = {
            'tikects': page_obj,
            'tikects_abiertos': tikects_abiertos,
            'tikects_cerrados': tikects_cerrados,
            'reasignados_ids': reasignados_ids,  # Cambio: usar set de IDs
            'es_superusuario': True,
        }
        return render(request, 'tickets/tikects_asignados_agentes.html', context)
    
    # Si no es superusuario, obtener el agente del usuario actual
    try:
        agente_actual = Agentes.objects.get(usuario=user)
    except Agentes.DoesNotExist:
        messages.warning(request, "No tienes un perfil de agente asignado.")
        return redirect('pagina_principal')
    
    tickets_base = Tickets.objects.filter(usuario=user).order_by('-fecha_creacion')
    tikects_cerrados = tickets_base.filter(estado__iexact='cerrado').count()
    tikects_abiertos = tickets_base.exclude(estado__iexact='cerrado').count()

    url_name = request.resolver_match.url_name
    if url_name == 'ver_tikects_asignados_agentes_cerrados':
        tickets_filtrados = tickets_base.filter(estado__iexact='cerrado')
    elif url_name == 'ver_tikects_asignados_agentes_abiertos':
        tickets_filtrados = tickets_base.exclude(estado__iexact='cerrado')
    else:
        tickets_filtrados = tickets_base

    paginator = Paginator(tickets_filtrados, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Crear un set de IDs de tickets reasignados para consulta rápida
    reasignados_ids = set()
    for r in ReasignacionTikects.objects.all():
        try:
            if r.agente_nuevo:
                reasignados_ids.add(r.ticket_id)
        except:
            pass

    context = {
        'tikects': page_obj,
        'tikects_abiertos': tikects_abiertos,
        'tikects_cerrados': tikects_cerrados,
        'reasignados_ids': reasignados_ids,  # Cambio: usar set de IDs
        'es_superusuario': False,
    }
    return render(request, 'tickets/tikects_asignados_agentes.html', context)


@login_required
def ver_tikects_asignados_agentes_cerrados(request):
    """Vista para agentes o superusuarios: ver tickets asignados CERRADOS"""
    user = request.user
    
    # Si es superusuario, mostrar todos los tickets cerrados
    if user.is_superuser:
        tickets_base = Tickets.objects.filter(estado__iexact='cerrado').order_by('-fecha_creacion')
        tikects_cerrados = tickets_base.count()
        tikects_abiertos = Tickets.objects.exclude(estado__iexact='cerrado').count()
        
        paginator = Paginator(tickets_base, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        reasignados_ids = set()
        for r in ReasignacionTikects.objects.all():
            try:
                if r.agente_nuevo:
                    reasignados_ids.add(r.ticket_id)
            except:
                pass

        context = {
            'tikects': page_obj,
            'tikects_abiertos': tikects_abiertos,
            'tikects_cerrados': tikects_cerrados,
            'reasignados_ids': reasignados_ids,
            'es_superusuario': True,
        }
        return render(request, 'tickets/tikects_asignados_agentes.html', context)
    
    # Obtener el agente del usuario actual
    try:
        agente_actual = Agentes.objects.get(usuario=user)
    except Agentes.DoesNotExist:
        messages.warning(request, "No tienes un perfil de agente asignado.")
        return redirect('pagina_principal')
    
    # Tickets creados por el agente
    tickets_totales_agente = Tickets.objects.filter(usuario=user)
    tikects_cerrados = tickets_totales_agente.filter(estado__iexact='cerrado').count()
    tikects_abiertos = tickets_totales_agente.exclude(estado__iexact='cerrado').count()
    
    # Tickets directos (creados por el agente como usuario)
    tikects_directos = Tickets.objects.filter(
        usuario=agente_actual.usuario, 
        estado='cerrado'
    ).order_by('-fecha_creacion')
    
    # Tickets reasignados al agente
    reasignaciones = ReasignacionTikects.objects.filter(agente_nuevo=agente_actual)
    tikects_reasignados = Tickets.objects.filter(
        id__in=[r.tikect.id for r in reasignaciones], 
        estado='cerrado'
    ).order_by('-fecha_creacion')
    
    # Tickets por servicio asignado al agente
    asignaciones_servicios = AsignacionTikects.objects.filter(agente=agente_actual)
    services_ids = [a.tikect.servicio.id for a in asignaciones_servicios if a.tikect and a.tikect.servicio]
    tikects_servicios = Tickets.objects.filter(
        servicio_id__in=services_ids, 
        estado='cerrado'
    ).order_by('-fecha_creacion')

    # Combinar y eliminar duplicados
    tikects_list = list(tikects_directos) + list(tikects_reasignados) + list(tikects_servicios)
    tikects_list = list(dict.fromkeys(tikects_list))
    tikects_list.sort(key=lambda x: x.fecha_creacion, reverse=True)

    paginator = Paginator(tikects_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    reasignados_ids = set()
    try:
        for r in ReasignacionTikects.objects.all():
            if r.agente_nuevo and r.agente_nuevo.usuario:
                reasignados_ids.add(r.tikect.id)
    except:
        pass

    return render(request, 'tickets/tikects_asignados_agentes.html', {
        'tikects': page_obj,
        'reasignados_ids': reasignados_ids,
        'tikects_abiertos': tikects_abiertos,
        'tikects_cerrados': tikects_cerrados,
        'es_superusuario': False,
    })


@login_required
def ver_tikects_asignados_agentes_abiertos(request):
    """Vista para agentes o superusuarios: ver tickets asignados ABIERTOS"""
    user = request.user
    
    # Si es superusuario, mostrar todos los tickets abiertos
    if user.is_superuser:
        tickets_base = Tickets.objects.exclude(estado__iexact='cerrado').order_by('-fecha_creacion')
        tikects_cerrados = Tickets.objects.filter(estado__iexact='cerrado').count()
        tikects_abiertos = tickets_base.count()
        
        paginator = Paginator(tickets_base, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        reasignados_ids = set()
        for r in ReasignacionTikects.objects.all():
            try:
                if r.agente_nuevo:
                    reasignados_ids.add(r.ticket_id)
            except:
                pass

        context = {
            'tikects': page_obj,
            'tikects_abiertos': tikects_abiertos,
            'tikects_cerrados': tikects_cerrados,
            'reasignados_ids': reasignados_ids,
            'es_superusuario': True,
        }
        return render(request, 'tickets/tikects_asignados_agentes.html', context)
    
    # Obtener el agente del usuario actual
    try:
        agente_actual = Agentes.objects.get(usuario=user)
    except Agentes.DoesNotExist:
        messages.warning(request, "No tienes un perfil de agente asignado.")
        return redirect('pagina_principal')
    
    # Tickets creados por el agente
    tickets_totales_agente = Tickets.objects.filter(usuario=user)
    tikects_cerrados = tickets_totales_agente.filter(estado__iexact='cerrado').count()
    tikects_abiertos = tickets_totales_agente.exclude(estado__iexact='cerrado').count()
    
    # Tickets directos (creados por el agente como usuario) - ABIERTOS
    tikects_directos = Tickets.objects.filter(
        usuario=agente_actual.usuario
    ).exclude(estado='cerrado').order_by('-fecha_creacion')
    
    # Tickets reasignados al agente - ABIERTOS
    reasignaciones = ReasignacionTikects.objects.filter(agente_nuevo=agente_actual)
    tikects_reasignados = Tickets.objects.filter(
        id__in=[r.tikect.id for r in reasignaciones]
    ).exclude(estado='cerrado').order_by('-fecha_creacion')
    
    # Tickets por servicio asignado al agente - ABIERTOS
    asignaciones_servicios = AsignacionTikects.objects.filter(agente=agente_actual)
    services_ids = [a.tikect.servicio.id for a in asignaciones_servicios if a.tikect and a.tikect.servicio]
    tikects_servicios = Tickets.objects.filter(
        servicio_id__in=services_ids
    ).exclude(estado='cerrado').order_by('-fecha_creacion')

    # Combinar y eliminar duplicados
    tikects_list = list(tikects_directos) + list(tikects_reasignados) + list(tikects_servicios)
    tikects_list = list(dict.fromkeys(tikects_list))
    tikects_list.sort(key=lambda x: x.fecha_creacion, reverse=True)
    
    paginator = Paginator(tikects_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    reasignados_ids = set()
    try:
        for r in ReasignacionTikects.objects.all():
            if r.agente_nuevo and r.agente_nuevo.usuario:
                reasignados_ids.add(r.tikect.id)
    except:
        pass

    return render(request, 'tickets/tikects_asignados_agentes.html', {
        'tikects': page_obj,
        'reasignados_ids': reasignados_ids,
        'tikects_abiertos': tikects_abiertos,
        'tikects_cerrados': tikects_cerrados,
        'es_superusuario': False,
    })

# ============================================
# TICKETS - DETALLE Y ACCIONES
# ============================================

@login_required
def detalle_tikect(request, tikect_id):
    tikect = get_object_or_404(Tickets, id=tikect_id)
    try:
        Notificaciones.objects.filter(tikect=tikect, agente__usuario=request.user).update(leida=True)
    except:
        pass

    if request.method == 'POST':
        tikect.estado = 'cerrado'
        tikect.save()
        if hasattr(request.user, 'agente'):
            return redirect('ver_tikects_asignados_agentes')
        else:
            return redirect('ver_tikects')

    reasignaciones = ReasignacionTikects.objects.filter(tikect=tikect)
    reasignado = False
    if reasignaciones.exists():
        agente_nuevo = reasignaciones.first().agente_nuevo
        if hasattr(request.user, 'agente') and agente_nuevo == request.user.agente:
            reasignado = True

    return render(request, 'tickets/detalle_tikect.html', {
        'tikect': tikect,
        'reasignado': reasignado
    })

@login_required
def cerrar_tikect(request, tikect_id):
    tikect = get_object_or_404(Tickets, id=tikect_id)
    if request.method == 'POST':
        descripcion_solucion = request.POST.get('descripcion_solucion')
        tikect.estado = 'cerrado'
        tikect.fecha_cierre = timezone.now()
        tikect.descripcion_solucion = descripcion_solucion
        
        if hasattr(request.user, 'agente'):
            tikect.cerrado_por_agente = request.user.agente
        else:
            tikect.cerrado_por_agente = Agentes.objects.filter(usuario=request.user).first()
            
        tikect.save()
        
        if tikect.usuario and tikect.usuario.email:
            asunto = f"Ticket Cerrado: #{tikect.id} - {tikect.titulo}"
            mensaje = f"Hola {tikect.usuario.first_name},\n\nTu ticket ha sido marcado como CERRADO.\nSolución aplicada: {descripcion_solucion}"
            try:
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
def reasignar_tikect(request, tikect_id):  # Asegurar que sea tikect_id
    ticket = get_object_or_404(Tickets, id=tikect_id)  # Usar tikect_id
    
    try:
        agente_actual = Agentes.objects.get(usuario=request.user)
    except Agentes.DoesNotExist:
        messages.error(request, "No tienes permisos para reasignar tickets. No eres un agente.")
        return redirect('detalle_tikect', tikect_id=ticket.id)  # Usar tikect_id

    if ReasignacionTikects.objects.filter(tikect=ticket, agente_nuevo=agente_actual).exists():
        messages.error(request, "Este ticket ya ha sido reasignado.")
        return redirect('detalle_tikect', tikect_id=ticket.id)

    grupo_agente_actual = Agentes_Por_Grupos.objects.filter(agente=agente_actual).first()
    if not grupo_agente_actual:
        messages.error(request, "No perteneces a ningún grupo resolutor.")
        return redirect('detalle_tikect', tikect_id=ticket.id)

    agentes_grupo = Agentes.objects.filter(
        agentes_por_grupos__grupo=grupo_agente_actual.grupo
    ).exclude(id=agente_actual.id)

    if request.method == 'POST':
        nuevo_agente_id = request.POST.get('nuevo_agente')
        if not nuevo_agente_id:
            messages.error(request, "Debe seleccionar un agente para reasignar.")
            return redirect('reasignar_tikect', tikect_id=ticket.id)  # Usar tikect_id
        
        try:
            nuevo_agente = Agentes.objects.get(id=nuevo_agente_id)
            ReasignacionTikects.objects.create(
                tikect=ticket,
                agente_anterior=agente_actual,
                agente_nuevo=nuevo_agente
            )
            Notificaciones.objects.create(
                tikect=ticket,
                agente=nuevo_agente,
                descripcion=f"Ticket reasignado desde {agente_actual.nombre_usuario}"
            )
            messages.success(request, f"Ticket reasignado exitosamente a {nuevo_agente.nombre_usuario}")
            return redirect('ver_tikects_asignados_agentes')
        except Exception as e:
            messages.error(request, f"Error al reasignar: {str(e)}")

    return render(request, 'reasignar_tikects.html', {
        'tikect': ticket,
        'agentes_grupo': agentes_grupo
    })

# ============================================
# TICKETS - CREACIÓN
# ============================================

@login_required
def crear_tikects_clientes(request):
    if request.method == 'GET':
        servicios = Tickets_Servicios.objects.all()
        gerencias = Gerencia.objects.all()
        return render(request, 'tickets/tikects_crear.html', {
            'servicios': servicios,
            'gerencias': gerencias,
        })
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        servicio_id = request.POST.get('servicio')
        usuario = request.user

        servicio = get_object_or_404(Tickets_Servicios, id=servicio_id)
        cliente = Cliente.objects.filter(usuario=usuario).first()

        nuevo_tikect = Tickets.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            servicio=servicio,
            usuario=usuario,
            cliente=cliente,
        )

        try:
            asignacion = AsignacionTikects.objects.get(servicio=servicio)
            if asignacion.agente_actual:
                Notificaciones.objects.create(
                    tikect=nuevo_tikect,
                    descripcion=f"Nuevo ticket '{titulo}'",
                    usuario_creador=usuario,
                    agent=asignacion.agente_actual
                )
        except:
            pass

        return redirect('ver_mis_tikects')
    return redirect('crear_tikects_clientes')

@login_required
def crear_tikects(request):
    if request.method == 'GET':
        servicios = Tickets_Servicios.objects.all()
        gerencias = Gerencia.objects.all()
        return render(request, 'tickets/tikects_crear.html', {
            'servicios': servicios,
            'gerencias': gerencias
        })
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        servicio_id = request.POST.get('servicio')
        usuario = request.user

        servicio = get_object_or_404(Tickets_Servicios, id=servicio_id)

        Tickets.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            servicio=servicio,
            usuario=usuario,
        )
        return redirect('ver_tikects')
    return redirect('crear_tikects')

# ============================================
# ESTADÍSTICAS Y EXPORTACIONES
# ============================================

@superuser_required
@login_required
def tikects_estadisticas(request):
    total_tikects = Tickets.objects.count()
    tikects_cerrados = Tickets.objects.filter(estado__iexact='cerrado').count()
    tikects_abiertos = Tickets.objects.exclude(estado='cerrado').count()
    servicios = Tickets.objects.values('servicio__nombre').annotate(count=Count('servicio'))

    porcentaje_abiertos = (tikects_abiertos / total_tikects * 100) if total_tikects > 0 else 0
    porcentaje_cerrados = (tikects_cerrados / total_tikects * 100) if total_tikects > 0 else 0

    tikects_por_dia_cerrados = Tickets.objects.filter(estado='cerrado').values('fecha_cierre__date').annotate(count=Count('id')).order_by('fecha_cierre__date')
    tikects_por_mes_cerrados = Tickets.objects.filter(estado='cerrado').annotate(month=TruncMonth('fecha_cierre')).values('month').annotate(count=Count('id')).order_by('month')
    tikects_por_semana_cerrados = Tickets.objects.filter(estado='cerrado').annotate(week=TruncWeek('fecha_cierre')).values('week').annotate(count=Count('id')).order_by('week')

    tickets_resueltos = Tickets.objects.filter(estado='cerrado', fecha_cierre__isnull=False)
    tiempo_promedio = 0
    if tickets_resueltos.exists():
        promedio_td = tickets_resueltos.aggregate(avg_time=Avg(F('fecha_cierre') - F('fecha_creacion')))['avg_time']
        if promedio_td:
            tiempo_promedio = round(promedio_td.total_seconds() / 3600, 1)

    tickets_por_prioridad = list(Tickets.objects.values('prioridad').annotate(count=Count('id')))

    tikects_por_agente = []
    try:
        agentes_ids = Tickets.objects.filter(estado='cerrado').exclude(cerrado_por_agente__isnull=True).values_list('cerrado_por_agente', flat=True).distinct()
        for agente_id in agentes_ids:
            try:
                user = User.objects.get(id=agente_id)
                count = Tickets.objects.filter(estado='cerrado', cerrado_por_agente_id=agente_id).count()
                tikects_por_agente.append({
                    'cerrado_por_agente__username': user.username,
                    'cerrado_por_agente__first_name': user.first_name,
                    'cerrado_por_agente__last_name': user.last_name,
                    'count': count
                })
            except User.DoesNotExist:
                pass
        tikects_por_agente = sorted(tikects_por_agente, key=lambda x: x['count'], reverse=True)
    except Exception as e:
        print(f"Error en estadísticas de agentes: {e}")

    context = {
        'total_tikects': total_tikects,
        'tikects_cerrados': tikects_cerrados,
        'tikects_abiertos': tikects_abiertos,
        'porcentaje_abiertos': porcentaje_abiertos,
        'porcentaje_cerrados': porcentaje_cerrados,
        'tiempo_promedio': tiempo_promedio,
        'tickets_por_prioridad': tickets_por_prioridad,
        'servicios': list(servicios),
        'tikects_por_dia_cerrados': list(tikects_por_dia_cerrados),
        'tikects_por_mes_cerrados': list(tikects_por_mes_cerrados),
        'tikects_por_semana_cerrados': list(tikects_por_semana_cerrados),
        'tikects_por_agente': list(tikects_por_agente),
    }
    return render(request, 'configuracion/estadisticas.html', context)

# ============================================
# EXPORTACIONES
# ============================================

@superuser_required
@login_required
def exportar_tikects_excel(request):
    servicio_seleccionado = request.GET.get('servicio', 'Todo')
    if servicio_seleccionado == 'Todo':
        tikects = Tickets.objects.filter(estado='cerrado')
    else:
        tikects = Tickets.objects.filter(estado='cerrado', servicio__nombre=servicio_seleccionado)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tickets Cerrados"

    headers = ['ID', 'Título', 'Descripción', 'Usuario', 'Servicio', 'Fecha Creación', 'Fecha Cierre', 'Solución', 'Agente que cerró', 'Gerencia']
    ws.append(headers)

    for t in tikects:
        ws.append([
            t.id,
            t.titulo,
            t.descripcion,
            t.usuario.username if t.usuario else '',
            t.servicio.nombre if t.servicio else '',
            t.fecha_creacion.strftime('%Y-%m-%d %H:%M') if t.fecha_creacion else '',
            t.fecha_cierre.strftime('%Y-%m-%d %H:%M') if t.fecha_cierre else '',
            t.descripcion_solucion or '',
            t.cerrado_por_agente.username if t.cerrado_por_agente else '',
            t.gerencia or ''
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=tickets_cerrados_{servicio_seleccionado}.xlsx'
    wb.save(response)
    return response

@superuser_required
@login_required
def exportar_tikects_pdf(request):
    servicio_seleccionado = request.GET.get('servicio', 'Todo')
    if servicio_seleccionado == 'Todo':
        tikects = Tickets.objects.filter(estado='cerrado')
    else:
        tikects = Tickets.objects.filter(estado='cerrado', servicio__nombre=servicio_seleccionado)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=tickets_cerrados_{servicio_seleccionado}.pdf'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    x, y = 50, height - 50
    line_height = 14

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, f"Tickets Cerrados - {servicio_seleccionado}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    headers = ['ID', 'Título', 'Usuario', 'Servicio', 'Fecha Cierre']
    col_widths = [40, 200, 100, 100, 80]
    x_pos = x
    for i, h in enumerate(headers):
        c.drawString(x_pos, y, h)
        x_pos += col_widths[i]
    y -= line_height

    c.setFont("Helvetica", 9)
    for t in tikects:
        x_pos = x
        c.drawString(x_pos, y, str(t.id))
        x_pos += col_widths[0]
        c.drawString(x_pos, y, t.titulo[:30] if t.titulo else '')
        x_pos += col_widths[1]
        c.drawString(x_pos, y, t.usuario.username[:15] if t.usuario else '')
        x_pos += col_widths[2]
        c.drawString(x_pos, y, t.servicio.nombre if t.servicio else '')
        x_pos += col_widths[3]
        c.drawString(x_pos, y, t.fecha_cierre.strftime('%Y-%m-%d') if t.fecha_cierre else '')
        y -= line_height
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 9)

    c.save()
    return response

# ============================================
# PERMISOS & NOTIFICACIONES
# ============================================

def check_notifications(request):
    if request.user.is_authenticated:
        agente = getattr(request.user, 'agente', None)
        if agente:
            nuevas = Notificaciones.objects.filter(agente=agente, leida=False)
            notificaciones = [{'tikect_id': n.tikect.id, 'descripcion': n.descripcion} for n in nuevas]
            return JsonResponse({'new_notifications': nuevas.exists(), 'notifications': notificaciones})
    return JsonResponse({'new_notifications': False, 'notifications': []})

def password_reset_view(request):
    return render(request, 'password_reset.html', {'step': 'form'})