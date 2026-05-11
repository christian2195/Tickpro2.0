#!/bin/bash
# Script de monitoreo del sistema

echo "=== MONITOREO DEL SISTEMA DE TICKETS ==="
echo ""

echo "📊 Estado de servicios:"
sudo systemctl status gunicorn --no-pager | grep "Active:"
sudo systemctl status nginx --no-pager | grep "Active:"
sudo systemctl status postgresql --no-pager | grep "Active:"

echo ""
echo "💾 Uso de disco:"
df -h /home/$USER

echo ""
echo "🧠 Uso de memoria:"
free -h

echo ""
echo "📈 Procesos de Gunicorn:"
ps aux | grep gunicorn | grep -v grep | wc -l

echo ""
echo "📝 Últimos errores (Gunicorn):"
sudo journalctl -u gunicorn -n 5 --no-pager

echo ""
echo "🔄 Últimos respaldos:"
ls -lth /home/$USER/backups/ 2>/dev/null | head -5

echo ""
echo "🌐 Conexiones activas:"
sudo netstat -tn | grep :80 | wc -l