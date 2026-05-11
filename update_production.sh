#!/bin/bash
# Script para actualizar la aplicación en producción

set -e

PROJECT_PATH="/home/$USER/sistema-de-tickets2"
BACKUP_PATH="/home/$USER/update_backup_$(date +%Y%m%d_%H%M%S)"

echo "=== ACTUALIZACIÓN DEL SISTEMA ==="

# 1. Crear backup antes de actualizar
echo "Creando backup previo a la actualización..."
mkdir -p $BACKUP_PATH
cp -r $PROJECT_PATH $BACKUP_PATH/

# 2. Activar entorno virtual
cd $PROJECT_PATH
source venv/bin/activate

# 3. Actualizar dependencias
echo "Actualizando dependencias..."
pip install --upgrade pip
pip install --upgrade django psycopg2-binary gunicorn

# 4. Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py makemigrations
python manage.py migrate

# 5. Recolectar archivos estáticos
echo "Actualizando archivos estáticos..."
python manage.py collectstatic --noinput

# 6. Reiniciar servicios
echo "Reiniciando servicios..."
sudo systemctl restart gunicorn
sudo systemctl reload nginx

# 7. Verificar estado
echo "Verificando estado..."
sudo systemctl status gunicorn --no-pager

echo "=== ACTUALIZACIÓN COMPLETADA ==="
echo "Backup guardado en: $BACKUP_PATH"