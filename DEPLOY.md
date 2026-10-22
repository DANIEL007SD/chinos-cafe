# Despliegue en NGINX / Linux — CHINOS CAFÉ S.A.

Guía de despliegue del servidor web (Parte I final del Examen Parcial 2).
**Todos los comandos se ejecutan DENTRO de la VM Linux (Ubuntu Server 22.04/24.04).**

Supuestos:
- Distro: **Ubuntu Server**.
- IP fija asignada al servidor: **172.20.10.100** (rango de la RED LAN de la Parte II).
- App servida en `http://172.20.10.100:8080` y `https://172.20.10.100:8443`.
- Usuario de la VM: `chinos` (ajusta a tu usuario real).

---

## Fase 0 — Actualizar el sistema e instalar paquetes

```bash
sudo apt update && sudo apt upgrade -y
```

```bash
sudo apt install -y python3 python3-venv python3-pip nginx git ufw openssh-server vsftpd knockd openssl net-tools
```

---

## Fase 1 — IP fija (netplan)

Averigua el nombre de tu interfaz (en VirtualBox suele ser `enp0s3`):

```bash
ip a
```

Edita el netplan (ajusta el nombre del archivo y la interfaz):

```bash
sudo nano /etc/netplan/01-netcfg.yaml
```

Contenido (reemplaza `enp0s3` por tu interfaz):

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: no
      addresses: [172.20.10.100/24]
      routes:
        - to: default
          via: 172.20.10.1
      nameservers:
        addresses: [172.20.10.1, 8.8.8.8]
```

Aplica:

```bash
sudo netplan apply
```

Verifica:

```bash
ip a && ping -c 2 172.20.10.1
```

---

## Fase 2 — Clonar la app y preparar el entorno

```bash
cd ~
git clone https://github.com/DANIEL007SD/chinos-cafe.git
cd chinos-cafe
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install waitress
```

Prueba rápida (Ctrl+C para detener):

```bash
.venv/bin/waitress-serve --listen=127.0.0.1:8000 --call app:create_app
```

---

## Fase 3 — Servicio systemd (que la app arranque sola)

```bash
sudo nano /etc/systemd/system/chinos.service
```

Contenido (ajusta `chinos` al usuario y a la ruta real):

```ini
[Unit]
Description=CHINOS CAFE S.A. - Flask (waitress)
After=network.target

[Service]
User=chinos
WorkingDirectory=/home/chinos/chinos-cafe
ExecStart=/home/chinos/chinos-cafe/.venv/bin/waitress-serve --listen=127.0.0.1:8000 --call app:create_app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activa e inicia:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now chinos
sudo systemctl status chinos --no-pager
```

---

## Fase 4 — Certificado HTTPS (autofirmado)

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/nginx/ssl/chinos.key \
  -out /etc/nginx/ssl/chinos.crt \
  -subj "/C=PA/ST=Veraguas/L=Santiago/O=ChinosCafe/CN=172.20.10.100"
```

---

## Fase 5 — NGINX como reverse proxy (HTTP 8080 + HTTPS 8443)

```bash
sudo nano /etc/nginx/sites-available/chinos
```

Contenido:

```nginx
server {
    listen 8080;
    server_name 172.20.10.100;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 8443 ssl;
    server_name 172.20.10.100;

    ssl_certificate     /etc/nginx/ssl/chinos.crt;
    ssl_certificate_key /etc/nginx/ssl/chinos.key;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Habilita el sitio, quita el default, valida y recarga:

```bash
sudo ln -s /etc/nginx/sites-available/chinos /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

Prueba desde la misma VM:

```bash
curl -I http://172.20.10.100:8080
curl -kI https://172.20.10.100:8443
```

---

## Fase 6 — Firewall (UFW)

```bash
sudo ufw allow 22/tcp      # SSH (lo cerraremos con port knocking en la Fase 9)
sudo ufw allow 21/tcp      # FTP
sudo ufw allow 8080/tcp    # HTTP app
sudo ufw allow 8443/tcp    # HTTPS app
sudo ufw enable
sudo ufw status numbered
```

---

## Fase 7 — Acceso SSH seguro

```bash
sudo systemctl enable --now ssh
sudo nano /etc/ssh/sshd_config
```

Recomendado dentro del archivo:

```
PermitRootLogin no
PasswordAuthentication yes   # cámbialo a 'no' si usas llaves
```

```bash
sudo systemctl restart ssh
```

Desde la laptop (Windows / otra VM) te conectas así:

```bash
ssh chinos@172.20.10.100
```

---

## Fase 8 — Servidor FTP (vsftpd)

```bash
sudo nano /etc/vsftpd.conf
```

Asegura estas líneas:

```
listen=YES
listen_ipv6=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
```

```bash
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd
```

---

## Fase 9 — Port Knocking (knockd) para SSH y FTP

Cerramos SSH (22) y FTP (21) por defecto y solo se abren tras la "secuencia de golpes".

```bash
sudo nano /etc/knockd.conf
```

Contenido:

```ini
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
```

Cierra los puertos por defecto y activa knockd:

```bash
sudo ufw delete allow 22/tcp
sudo ufw delete allow 21/tcp
sudo nano /etc/default/knockd        # pon START_KNOCKD=1 y KNOCKD_OPTS="-i enp0s3"
sudo systemctl enable --now knockd
sudo systemctl status knockd --no-pager
```

Desde el cliente, para abrir SSH antes de conectarte (instala `knock` o usa nmap):

```bash
knock 172.20.10.100 7000 8000 9000 && ssh chinos@172.20.10.100
```

---

## Verificación final

```bash
sudo systemctl status chinos nginx ssh vsftpd knockd --no-pager
```

Abre en el navegador de la otra laptop (misma RED LAN):
- `http://172.20.10.100:8080`
- `https://172.20.10.100:8443`  (acepta la advertencia del certificado autofirmado)

> 📸 Toma capturas con fecha/hora de cada fase para la entrega.
```
