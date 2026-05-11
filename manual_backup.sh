#!/bin/bash
# Script de respaldo manual

BACKUP_DIR="/home/$USER/backups_manual"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_PATH="/home/$USER/sistema-de-tickets2"

mkdir -p $BACKUP_DIR

# Respaldo de base de datos
echo "Respaldando base de datos..."
PGPASSWORD='Tecno/*2025' pg_dump -h localhost -U django_user tikectsbd > "$BACKUP_DIR/tikects_$DATE.sql"

# Respaldo de archivos media
echo "Respaldando archivos media..."
tar -czf "$BACKUP_DIR/media_$DATE.tar.gz" $PROJECT_PATH/media 2>/dev/null

# Respaldo de configuración
echo "Respaldando configuración..."
cp $PROJECT_PATH/.env "$BACKUP_DIR/env_$DATE.bak" 2>/dev/null

echo "Respaldo completado en: $BACKUP_DIR"
ls -lh $BACKUP_DIR