#!/bin/bash
#================================================================
# SCRIPT DE INSTALACIÓN EN PRODUCCIÓN - SISTEMA DE TICKETS
# Versión: 1.0.0
# Fecha: Mayo 2026
#================================================================

set -e  # Detener el script si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables de configuración
PROJECT_NAME="sistema-de-tickets2"
PROJECT_PATH="/home/$USER/$PROJECT_NAME"
VENV_PATH="$PROJECT_PATH/venv"
DB_NAME="tikectsbd"
DB_USER="django_user"
DB_PASSWORD="Tecno/*2025"
DOMAIN="localhost"  # Cambiar por tu dominio
APP_PORT="8000"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Instalación del Sistema de Tickets${NC}"
echo -e "${GREEN}========================================${NC}"

# 1. Actualizar sistema
echo -e "${YELLOW}[1/10] Actualizando sistema...${NC}"
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias del sistema
echo -e "${YELLOW}[2/10] Instalando dependencias del sistema...${NC}"
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y postgresql postgresql-contrib libpq-dev
sudo apt install -y nginx curl git supervisor
sudo apt install -y build-essential libssl-dev libffi-dev

# 3. Configurar PostgreSQL
echo -e "${YELLOW}[3/10] Configurando PostgreSQL...${NC}"
sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql <<EOF
DROP DATABASE IF EXISTS $DB_NAME;
DROP USER IF EXISTS $DB_USER;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER USER $DB_USER WITH SUPERUSER;
CREATE DATABASE $DB_NAME OWNER $DB_USER;
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
GRANT CREATE ON SCHEMA public TO $DB_USER;
ALTER SCHEMA public OWNER TO $DB_USER;
\q
EOF

echo -e "${GREEN}✓ PostgreSQL configurado correctamente${NC}"

# 4. Crear estructura del proyecto
echo -e "${YELLOW}[4/10] Creando estructura del proyecto...${NC}"
cd /home/$USER
if [ -d "$PROJECT_PATH" ]; then
    echo -e "${YELLOW}El proyecto ya existe. Haciendo backup...${NC}"
    mv $PROJECT_PATH ${PROJECT_PATH}_backup_$(date +%Y%m%d_%H%M%S)
fi

mkdir -p $PROJECT_PATH
cd $PROJECT_PATH

# 5. Crear entorno virtual
echo -e "${YELLOW}[5/10] Creando entorno virtual...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel

# 6. Instalar dependencias de Python
echo -e "${YELLOW}[6/10] Instalando dependencias de Python...${NC}"
pip install django==4.2.11
pip install psycopg2-binary
pip install gunicorn
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install pillow
pip install whitenoise

# Crear requirements.txt
pip freeze > requirements.txt

# 7. Crear archivo settings.py optimizado para producción
echo -e "${YELLOW}[7/10] Configurando Django para producción...${NC}"

# Crear estructura del proyecto Django
django-admin startproject tikects_proyecto .
django-admin startapp tikects_app

# Configurar settings.py para producción
cat > tikects_proyecto/settings.py <<'SETTINGS'
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4!m$e3i1(-dk91bk2lcgnlbt-a8#rq_b&-i&dyp1!q4cs258n6')
DEBUG = False
ALLOWED_HOSTS = [os.environ.get('DOMAIN', 'localhost'), 'www.localhost', '127.0.0.1']

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'tikects_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tikects_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tikects_proyecto.wsgi.application'

# Base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'tikectsbd'),
        'USER': os.environ.get('DB_USER', 'django_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Tecno/*2025'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Caracas'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [BASE_DIR / 'tikects_app/static']

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_ID = 1

# Configuración de seguridad para producción
SECURE_SSL_REDIRECT = False  # Cambiar a True si usas HTTPS
SESSION_COOKIE_SECURE = False  # Cambiar a True si usas HTTPS
CSRF_COOKIE_SECURE = False  # Cambiar a True si usas HTTPS
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SETTINGS

# 8. Configurar URLs y archivos básicos
echo -e "${YELLOW}[8/10] Configurando URLs y archivos básicos...${NC}"

cat > tikects_proyecto/urls.py <<'URLS'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tikects_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
URLS

# Crear urls.py para la app
cat > tikects_app/urls.py <<'APPURLS'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

APPURLS

# Crear views básico
cat > tikects_app/views.py <<'VIEWS'
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Sistema de Tickets funcionando correctamente!")
VIEWS

# 9. Configurar Gunicorn como servicio
echo -e "${YELLOW}[9/10] Configurando Gunicorn...${NC}"

sudo bash -c "cat > /etc/systemd/system/gunicorn.service <<GUNICORN
[Unit]
Description=Gunicorn instance for Ticket System
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_PATH
Environment='PATH=$VENV_PATH/bin'
Environment='DJANGO_SECRET_KEY=django-insecure-4!m$e3i1(-dk91bk2lcgnlbt-a8#rq_b&-i&dyp1!q4cs258n6'
Environment='DB_NAME=$DB_NAME'
Environment='DB_USER=$DB_USER'
Environment='DB_PASSWORD=$DB_PASSWORD'
ExecStart=$VENV_PATH/bin/gunicorn --workers 3 --bind unix:$PROJECT_PATH/tikects.sock tikects_proyecto.wsgi:application

[Install]
WantedBy=multi-user.target
GUNICORN"

# 10. Configurar Nginx
echo -e "${YELLOW}[10/10] Configurando Nginx...${NC}"

sudo bash -c "cat > /etc/nginx/sites-available/tikects <<NGINX
server {
    listen 80;
    server_name $DOMAIN;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $PROJECT_PATH;
    }
    
    location /media/ {
        root $PROJECT_PATH;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_PATH/tikects.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX"

# Activar sitio de Nginx
sudo ln -sf /etc/nginx/sites-available/tikects /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

# 11. Configurar firewall
echo -e "${YELLOW}Configurando firewall...${NC}"
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 12. Configurar variables de entorno
echo -e "${YELLOW}Configurando variables de entorno...${NC}"
cat > $PROJECT_PATH/.env <<ENV
DJANGO_SECRET_KEY=django-insecure-4!m$e3i1(-dk91bk2lcgnlbt-a8#rq_b&-i&dyp1!q4cs258n6
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DOMAIN=$DOMAIN
ENV

# 13. Ejecutar migraciones y recolectar archivos estáticos
echo -e "${GREEN}Ejecutando migraciones y configuración final...${NC}"
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# 14. Crear superusuario automáticamente
echo -e "${YELLOW}Creando superusuario...${NC}"
python manage.py shell <<PYTHON
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
    print('Superusuario creado: admin / Admin123!')
PYTHON

# 15. Configurar permisos
echo -e "${YELLOW}Configurando permisos...${NC}"
sudo chown -R $USER:www-data $PROJECT_PATH
sudo chmod -R 755 $PROJECT_PATH
sudo chmod 664 $PROJECT_PATH/db.sqlite3 2>/dev/null || true

# 16. Iniciar servicios
echo -e "${GREEN}Iniciando servicios...${NC}"
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager

# 17. Configurar respaldo automático
echo -e "${YELLOW}Configurando respaldo automático...${NC}"
cat > ~/backup_tickets.sh <<BACKUP
#!/bin/bash
BACKUP_DIR="/home/$USER/backups"
DATE=\$(date +%Y%m%d_%H%M%S)
mkdir -p \$BACKUP_DIR
PGPASSWORD='$DB_PASSWORD' pg_dump -h localhost -U $DB_USER $DB_NAME > "\$BACKUP_DIR/tikects_\$DATE.sql"
tar -czf "\$BACKUP_DIR/media_\$DATE.tar.gz" $PROJECT_PATH/media 2>/dev/null || true
find \$BACKUP_DIR -type f -mtime +30 -delete
echo "Backup completado: \$DATE"
BACKUP

chmod +x ~/backup_tickets.sh
(crontab -l 2>/dev/null; echo "0 2 * * * /home/$USER/backup_tickets.sh") | crontab -

# 18. Resumen final
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}¡INSTALACIÓN COMPLETADA CON ÉXITO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "🌐 Aplicación: http://$DOMAIN"
echo -e "🔧 Panel Admin: http://$DOMAIN/admin"
echo -e "👤 Usuario: admin"
echo -e "🔑 Contraseña: Admin123!"
echo -e ""
echo -e "📁 Directorio: $PROJECT_PATH"
echo -e "🔄 Respaldo diario: ~/backups/"
echo -e ""
echo -e "Comandos útiles:"
echo -e "  sudo systemctl status gunicorn  # Ver estado"
echo -e "  sudo journalctl -u gunicorn -f  # Ver logs"
echo -e "  sudo systemctl restart gunicorn # Reiniciar"
echo -e "  ./backup_tickets.sh             # Respaldo manual"
echo -e "${GREEN}========================================${NC}"