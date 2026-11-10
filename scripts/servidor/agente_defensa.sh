#!/bin/bash
# =============================================================================
#  AGENTE DE DEFENSA — CHINOS CAFÉ S.A.
#  Monitoreo pasivo + auto-recuperación del servicio Flask + alertas JSONL.
#  Diseñado para ejecutarse como systemd unit (ver agente-defensa.service).
# =============================================================================
set -u

SERVICIO="${SERVICIO:-chinos}"
INTERVALO="${INTERVALO:-30}"
LOG_DIR="${LOG_DIR:-/var/log/chinos}"
LOG="${LOG_DIR}/defensa.jsonl"
URL_SALUD="${URL_SALUD:-http://127.0.0.1:8080/}"
NGINX_ACCESS="${NGINX_ACCESS:-/var/log/nginx/access.log}"
AUTH_LOG="${AUTH_LOG:-/var/log/auth.log}"

mkdir -p "$LOG_DIR"

emitir() {
  # emitir <nivel> <evento> <detalle>
  local nivel="$1" evento="$2" detalle="$3"
  printf '{"ts":"%s","nivel":"%s","evento":"%s","detalle":"%s"}\n' \
    "$(date -u '+%FT%TZ')" "$nivel" "$evento" "$(echo "$detalle" | tr -d '"')" \
    >> "$LOG"
}

verificar_servicio() {
  if ! systemctl is-active --quiet "$SERVICIO"; then
    emitir "ERROR" "servicio_caido" "systemctl start $SERVICIO"
    systemctl restart "$SERVICIO" && emitir "INFO" "servicio_reiniciado" "$SERVICIO"
    return
  fi
  if ! curl -fs --max-time 3 "$URL_SALUD" >/dev/null; then
    emitir "WARN" "salud_http_fail" "$URL_SALUD no responde"
  fi
}

detectar_hydra() {
  local n
  n=$(grep -c "Failed password" "$AUTH_LOG" 2>/dev/null || echo 0)
  if (( n > 20 )); then
    emitir "WARN" "posible_bruteforce_ssh" "Failed password count=$n"
  fi
}

detectar_rafaga_http() {
  # cuenta los últimos 500 hits por IP; >100 en la ventana = ráfaga
  local sospechosas
  sospechosas=$(tail -n 500 "$NGINX_ACCESS" 2>/dev/null \
    | awk '{print $1}' | sort | uniq -c | sort -rn \
    | awk '$1>100 {print $2":"$1}' | tr '\n' ',' )
  [[ -n "$sospechosas" ]] && emitir "WARN" "rafaga_http" "$sospechosas"
}

principal() {
  emitir "INFO" "arranque" "agente_defensa iniciado"
  while true; do
    verificar_servicio
    detectar_hydra
    detectar_rafaga_http
    sleep "$INTERVALO"
  done
}

principal "$@"
