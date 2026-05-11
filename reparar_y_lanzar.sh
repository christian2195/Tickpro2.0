#!/bin/bash

# =====================================================================
# SCRIPT DE REPARACIÓN CON LLAMADO DIRECTO AL VENV
# =====================================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Iniciando reparación forzada...${NC}"

# 1. Definir rutas de Python del entorno virtual
PYTHON_VENV="./venv/bin/python3"
PIP_VENV="./venv/bin/pip3"

# Si no existe el entorno, lo creamos de cero
if [ ! -f "$PYTHON_VENV" ]; then
    echo -e "${RED}❌ No se detectó Python en venv. Reinstalando entorno...${NC}"
    python3 -m venv venv
fi

# 2. Asegurar que Django esté instalado en ese venv específico
echo -e "${GREEN}📦 Asegurando dependencias en el entorno...${NC}"
$PIP_VENV install --upgrade pip
$PIP_VENV install django

# 3. Aplicar el parche al modelo para el error de fecha_creacion
echo -e "${GREEN}🔧 Corrigiendo el modelo 'agentes'...${NC}"
MODELS_FILE="tikects_app/models.py"
if [ -f "$MODELS_FILE" ]; then
    # Esta línea soluciona el error de auto_now_add 
    sed -i "s/fecha_creacion = models.DateTimeField(auto_now_add=True)/fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)/g" "$MODELS_FILE"
    echo -e "${GREEN}✅ models.py actualizado.${NC}"
fi

# 4. Limpiar migraciones y ejecutar con el Python del venv
echo -e "${GREEN}🧹 Limpiando migraciones antiguas...${NC}"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

echo -e "${YELLOW}⚙️  Ejecutando migraciones...${NC}"
$PYTHON_VENV manage.py makemigrations tikects_app
$PYTHON_VENV manage.py migrate

# 5. Lanzar el servidor
echo -e "${GREEN}🚀 Arrancando servidor...${NC}"
$PYTHON_VENV manage.py runserver 0.0.0.0:8000
