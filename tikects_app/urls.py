from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('', views.inicio, name='login'),
    path('inicio/', views.pagina_principal, name='pagina_principal'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('configuracion/', views.configuracion, name='configuracion'),

    # ============================================
    # GESTIÓN DE AGENTES (UNIFICADO)
    # ============================================
    path('gestion/agentes/', views.gestion_agentes, name='gestion_agentes'),
    path('gestion/agentes/eliminar/<int:agente_id>/', views.eliminar_agente, name='eliminar_agente'),

    # ============================================
    # GESTIÓN DE GRUPOS (UNIFICADO)
    # ============================================
    path('gestion/grupos/', views.gestion_grupos, name='gestion_grupos'),
    path('gestion/grupos/eliminar/<int:grupo_id>/', views.eliminar_grupo, name='eliminar_grupo'),
    path('gestion/grupos/asignar/', views.asignar_agente_grupo, name='asignar_agente_grupo'),
    path('gestion/grupos/quitar/<int:grupo_agente_id>/', views.quitar_agente_grupo, name='quitar_agente_grupo'),

    # ============================================
    # GESTIÓN DE AGENTES GENÉRICOS (UNIFICADO)
    # ============================================
    path('gestion/genericos/', views.gestion_genericos, name='gestion_genericos'),
    path('gestion/genericos/eliminar/<int:asignacion_id>/', views.eliminar_asignacion_generica, name='eliminar_asignacion_generica'),

    # ============================================
    # GESTIÓN DE PERMISOS (UNIFICADO)
    # ============================================
    path('gestion/permisos/', views.gestion_permisos, name='gestion_permisos'),

    # ============================================
    # GESTIÓN DE GERENCIAS (UNIFICADO)
    # ============================================
    path('gestion/gerencias/', views.gestion_gerencias, name='gestion_gerencias'),
    path('gestion/gerencias/eliminar/<int:gerencia_id>/', views.eliminar_gerencia, name='eliminar_gerencia'),

    # ============================================
    # SERVICIOS Y RESPUESTAS AUTOMÁTICAS
    # ============================================
    path('gestion/servicios/', views.tikects_servicios, name='tikects_servicios'),
    path('gestion/respuestas/', views.tikects_respuestas_automaticas, name='tikects_respuestas_automaticas'),
    path('gestion/servicios/crear/', views.tikects_servicios_crear, name='tikects_servicios_crear'),
    path('gestion/respuestas/crear/', views.tikects_respuestas_automaticas_crear, name='tikects_respuestas_automaticas_crear'),
    path('servicios/editar/<int:servicio_id>/', views.editar_servicios, name='editar_servicio'),
    path('servicios/eliminar/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('respuestas_automaticas/eliminar/<int:respuesta_id>/', views.eliminar_respuesta_automatica, name='eliminar_respuesta_automatica'),

    # ============================================
    # CLIENTES
    # ============================================
    path('clientes/ver/', views.clientes, name='ver_cliente'),
    path('clientes/crear/', views.crear_clientes, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/grupos/', views.usuarios_clientes_grupos, name='usuarios_clientes_grupos'),
    path('clientes/grupos/crear/', views.usuarios_clientes_grupos_crear, name='crear_grupo'),
    path('clientes/grupos/editar/<int:grupo_id>/', views.editar_grupo_clientes, name='editar_grupo_clientes'),
    path('clientes/grupos/eliminar/<int:grupo_id>/', views.eliminar_grupo_clientes, name='eliminar_grupo_clientes'),
    

    # ============================================
    # TICKETS - VISTAS PRINCIPALES
    # ============================================
    path('tikects/ver_todos/', views.ver_tikects, name='ver_tikects'),
    path('tikects/ver_todos/cerrados/', views.ver_tikects_cerrados, name='ver_tikects_cerrados'),
    path('tikects/ver_todos/abiertos/', views.ver_tikects_abiertos, name='ver_tikects_abiertos'),
    path('tikects/detalle/<int:tikect_id>/', views.detalle_tikect, name='detalle_tikect'),
    path('tikects/<int:tikect_id>/cerrar/', views.cerrar_tikect, name='cerrar_tikect'),
    path('tikects/crear/', views.crear_tikects, name='crear_tikects'),
    path('tikects/reasignar/<int:tikect_id>/', views.reasignar_tikect, name='reasignar_tikect'),

    # ============================================
    # TICKETS - CLIENTES
    # ============================================
    path('tikects/mis-tickets/', views.ver_mis_tikects, name='ver_mis_tikects'),
    path('tikects/mis-tickets/cerrados/', views.ver_mis_tikects_cerrados, name='ver_mis_tikects_cerrados'),
    path('tikects/mis-tickets/abiertos/', views.ver_mis_tikects_abiertos, name='ver_mis_tikects_abiertos'),
    path('tikects/crear-cliente/', views.crear_tikects_clientes, name='crear_tikects_clientes'),

    # ============================================
    # TICKETS - AGENTES
    # ============================================
    path('tikects/asignados/', views.ver_tikects_asignados_agentes, name='ver_tikects_asignados_agentes'),
    path('tikects/asignados/cerrados/', views.ver_tikects_asignados_agentes_cerrados, name='ver_tikects_asignados_agentes_cerrados'),
    path('tikects/asignados/abiertos/', views.ver_tikects_asignados_agentes_abiertos, name='ver_tikects_asignados_agentes_abiertos'),

    # ============================================
    # ESTADÍSTICAS Y EXPORTACIONES
    # ============================================
    path('estadisticas/', views.tikects_estadisticas, name='estadisticas'),
    path('exportar/excel/', views.exportar_tikects_excel, name='exportar_tikects_excel'),
    path('exportar/pdf/', views.exportar_tikects_pdf, name='exportar_tikects_pdf'),

    # ============================================
    # NOTIFICACIONES
    # ============================================
    path('notificaciones/check/', views.check_notifications, name='check_notifications'),

    # ============================================
    # RECUPERACIÓN DE CONTRASEÑA (UNIFICADO)
    # ============================================
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset.html',
        extra_context={'step': 'done'}
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset.html',
        extra_context={'step': 'confirm'}
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset.html',
        extra_context={'step': 'complete'}
    ), name='password_reset_complete'),
]