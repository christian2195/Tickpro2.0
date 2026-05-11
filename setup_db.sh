#!/bin/bash
# Script para configurar PostgreSQL correctamente

cd ~/sistema-de-tickets2
source venv/bin/activate

echo "=== Configurando PostgreSQL ==="

# 1. Eliminar y recrear base de datos
sudo -u postgres psql <<'EOF'
DROP DATABASE IF EXISTS tikectsbd;
DROP USER IF EXISTS django_user;
CREATE USER django_user WITH PASSWORD 'Tecno/*2025';
ALTER USER django_user WITH SUPERUSER;
CREATE DATABASE tikectsbd OWNER django_user;
GRANT ALL PRIVILEGES ON DATABASE tikectsbd TO django_user;
\c tikectsbd
GRANT ALL ON SCHEMA public TO django_user;
GRANT CREATE ON SCHEMA public TO django_user;
ALTER SCHEMA public OWNER TO django_user;
\q
EOF

echo "=== Base de datos configurada ==="

# 2. Probar conexión
PGPASSWORD='Tecno/*2025' psql -h 127.0.0.1 -U django_user -d tikectsbd -c "SELECT current_user, current_database();"

# 3. Ejecutar migraciones
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Iniciar servidor
python manage.py runserver 0.0.0.0:8000