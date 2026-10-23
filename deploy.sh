#!/usr/bin/env bash
# =====================================================================
# Despliegue automatizado de CHINOS CAFE S.A. en NGINX / Linux
# Examen Parcial 2 - Ingenieria Web (UTP) - Parte I (final)
#
# Uso (como root, dentro de la VM):
#   cd ~/chinos-cafe && git pull && sudo bash deploy.sh
#
# Deja la app corriendo con waitress (127.0.0.1:8000) detras de NGINX,
# accesible por HTTP 8080 y HTTPS 8443 en todas las interfaces.
# Configura ademas FTP (vsftpd) y Port Knocking (knockd).
#
# NOTA: no toca la red (netplan/IP fija) para no cortar la conexion.
# La IP fija de la RED LAN (172.20.10.100) se aplica aparte, ver DEPLOY.md.
# =====================================================================
set -u
APP_DIR="/root/chinos-cafe"
VENV="$APP_DIR/.venv"
log() { echo -e "\n\033[1;32m==> $*\033[0m"; }
warn() { echo -e "\033[1;33m[!] $*\033[0m"; }

# --------------------------------------------------------------
log "Fase 0: Paquetes"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y nginx vsftpd knockd openssl ufw openssh-server python3-venv

# --------------------------------------------------------------
log "Fase 1: Entorno Python + waitress"
if [ ! -d "$VENV" ]; then
  python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install -q -r "$APP_DIR/requirements.txt" waitress

# --------------------------------------------------------------
log "Fase 2: Servicio systemd (app con waitress)"
cat > /etc/systemd/system/chinos.service <<EOF
[Unit]
Description=CHINOS CAFE S.A. - Flask (waitress)
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
ExecStart=$VENV/bin/waitress-serve --listen=127.0.0.1:8001 --call app:create_app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl unmask chinos.service 2>/dev/null || true
systemctl daemon-reload
systemctl enable --now chinos.service

# --------------------------------------------------------------
log "Fase 3: Certificado HTTPS autofirmado"
mkdir -p /etc/nginx/ssl
if [ ! -f /etc/nginx/ssl/chinos.crt ]; then
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/chinos.key \
    -out /etc/nginx/ssl/chinos.crt \
    -subj "/C=PA/ST=Veraguas/L=Santiago/O=ChinosCafe/CN=172.20.10.100"
fi

# --------------------------------------------------------------
log "Fase 4: NGINX reverse proxy (HTTP 8080 + HTTPS 8443)"
cat > /etc/nginx/sites-available/chinos <<'EOF'
server {
    listen 8080;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
server {
    listen 8443 ssl;
    server_name _;
    ssl_certificate     /etc/nginx/ssl/chinos.crt;
    ssl_certificate_key /etc/nginx/ssl/chinos.key;
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
ln -sf /etc/nginx/sites-available/chinos /etc/nginx/sites-enabled/chinos
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx && systemctl enable nginx

# --------------------------------------------------------------
log "Fase 5: Firewall (UFW) - puertos abiertos"
ufw allow 22/tcp
ufw allow 21/tcp
ufw allow 8080/tcp
ufw allow 8443/tcp
ufw allow 30000:30100/tcp   # rango pasivo FTP
yes | ufw enable

# --------------------------------------------------------------
log "Fase 6: FTP (vsftpd)"
cat > /etc/vsftpd.conf <<'EOF'
listen=YES
listen_ipv6=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
pasv_enable=YES
pasv_min_port=30000
pasv_max_port=30100
EOF
systemctl restart vsftpd && systemctl enable vsftpd

# --------------------------------------------------------------
log "Fase 7: Port Knocking (knockd) - configuracion"
cat > /etc/knockd.conf <<'EOF'
[options]
    UseSyslog

[openSSH]
    sequence    = 7000,8000,9000
    seq_timeout = 5
    command     = /usr/sbin/ufw allow from %IP% to any port 22
    tcpflags    = syn

[closeSSH]
    sequence    = 9000,8000,7000
    seq_timeout = 5
    command     = /usr/sbin/ufw delete allow from %IP% to any port 22
    tcpflags    = syn

[openFTP]
    sequence    = 7100,8100,9100
    seq_timeout = 5
    command     = /usr/sbin/ufw allow from %IP% to any port 21
    tcpflags    = syn
EOF
# Se deja knockd instalado y configurado. NO se cierran los puertos aqui
# para evitar perder el acceso. Para activarlo en la demo, ver DEPLOY.md.
warn "knockd configurado pero NO activado (evita bloqueo). Activacion manual en DEPLOY.md."

# --------------------------------------------------------------
log "Verificacion"
echo "Servicios:"; systemctl is-active chinos nginx vsftpd
echo; echo "Prueba local:"; sleep 1
curl -sI http://127.0.0.1:8080 | head -1
curl -skI https://127.0.0.1:8443 | head -1
echo
IPS=$(hostname -I)
log "LISTO. App accesible en: http://<IP>:8080  y  https://<IP>:8443"
echo "IP(s) de esta VM: $IPS"
