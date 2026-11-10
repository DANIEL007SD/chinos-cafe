#!/bin/bash
# =============================================================================
#  BACKUP_DB — CHINOS CAFÉ S.A.
#  Snapshot periódico de la BD principal SQLite.
#  Programar en cron:  */5 * * * * /usr/local/bin/backup_db.sh
# =============================================================================
set -eu

APP_DIR="${APP_DIR:-/home/chinos/app}"
DB="$APP_DIR/chinos_cafe.db"
DESTINO="${DESTINO:-$HOME/backup-db}"
RETENCION_HORAS=24

mkdir -p "$DESTINO"
ts=$(date '+%Y%m%d_%H%M%S')
destino_file="$DESTINO/chinos_cafe_${ts}.db"

# Uso de .backup para consistencia incluso con escrituras concurrentes
if command -v sqlite3 >/dev/null; then
  sqlite3 "$DB" ".backup '$destino_file'"
else
  cp -p "$DB" "$destino_file"
fi

# Rotación: borra respaldos de más de N horas
find "$DESTINO" -maxdepth 1 -name 'chinos_cafe_*.db' -mmin +$((RETENCION_HORAS*60)) -delete

echo "[OK] Respaldo creado: $destino_file"
