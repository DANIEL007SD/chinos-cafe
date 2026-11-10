#!/bin/bash
# =============================================================================
#  SUITE DE AUDITORÍA — PARCIAL 2 (KALI LINUX)
#  CHINOS CAFÉ S.A. — Ingeniería Web, UTP
#  Autor: Edrian Hiraldo (Laptop B)
# =============================================================================
#  Reglas (ver PLAN_EQUIPO.md §6):
#   * Solo se ataca lo autorizado por el profesor.
#   * Nada fuera del rango 172.20.10.0/24.
#   * Toda acción queda registrada en audit.log con fecha y hora.
# =============================================================================
set -u

OBJETIVO="${OBJETIVO:-172.20.10.100}"
RANGO_PERMITIDO="172.20.10."
BASE="$HOME/auditoria_parcial2"
EVID="$BASE/evidencias"
AUDIT_LOG="$BASE/audit.log"
USERS="$BASE/usuarios.txt"
PASSWORDS="$BASE/passwords.txt"

mkdir -p "$EVID"

# --- Validación de alcance -------------------------------------------------
validar_objetivo() {
  if [[ ! "$OBJETIVO" =~ ^${RANGO_PERMITIDO//./\\.} ]]; then
    echo "[ABORTADO] IP $OBJETIVO fuera del rango autorizado ($RANGO_PERMITIDO/24)." >&2
    exit 2
  fi
}

registrar() {
  # registrar <nombre_prueba> <comando_resumen>
  printf '%s | %s | %s | %s\n' \
    "$(date '+%Y-%m-%d %H:%M:%S')" "$OBJETIVO" "$1" "$2" >> "$AUDIT_LOG"
}

ejecutar() {
  # ejecutar <nombre_prueba> <comando...>
  local nombre="$1"; shift
  local ts; ts=$(date '+%Y%m%d_%H%M%S')
  local salida="$EVID/${ts}_${nombre}.txt"
  {
    echo "===== $(date '+%F %T') | $nombre =====";
    echo "Comando: $*"; echo;
    "$@" 2>&1
    echo; echo "===== fin ====="
  } | tee "$salida"
  registrar "$nombre" "$*"
}

menu() {
  cat <<EOF

  SUITE DE AUDITORÍA — PARCIAL 2 (KALI LINUX)
  Objetivo Servidor: $OBJETIVO
  -----------------------------------------------------------
  1) Escaneo de Puertos NMAP (Antes de Port Knocking)
  2) Enviar secuencia Port Knocking (Desbloquear SSH/FTP)
  3) Escaneo NMAP (Después de Port Knocking)
  4) Prueba de Fuerza Bruta Hydra (SSH)
  5) Prueba de Rate-Limiting / DoS liviano (NGINX)
  6) Probar conectividad HTTP (8080) y HTTPS (8443)
  7) Captura tcpdump (10 s)
  0) Salir
EOF
}

main() {
  validar_objetivo
  touch "$AUDIT_LOG"
  while true; do
    menu
    read -rp $'\nSelecciona una opción [0-7]: ' opt
    case "$opt" in
      1) ejecutar "nmap_pre" nmap -sS -Pn -p 21,22,80,8080,8443 "$OBJETIVO" ;;
      2) ejecutar "knock_ssh" knock -v "$OBJETIVO" 7000 8000 9000
         ejecutar "knock_ftp" knock -v "$OBJETIVO" 7100 8100 9100 ;;
      3) ejecutar "nmap_post" nmap -sS -Pn -p 21,22,80,8080,8443 "$OBJETIVO" ;;
      4) ejecutar "hydra_ssh" hydra -L "$USERS" -P "$PASSWORDS" -t 4 -f \
           ssh://"$OBJETIVO" ;;
      5) ejecutar "ab_nginx" ab -n 2000 -c 50 "http://$OBJETIVO:8080/" ;;
      6) ejecutar "curl_http"  curl -sI "http://$OBJETIVO:8080/"
         ejecutar "curl_https" curl -skI "https://$OBJETIVO:8443/" ;;
      7) ejecutar "tcpdump_10s" timeout 10 tcpdump -i any -c 200 host "$OBJETIVO" ;;
      0) echo "Saliendo..."; exit 0 ;;
      *) echo "Opción inválida" ;;
    esac
  done
}

main "$@"
