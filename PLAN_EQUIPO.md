# PLAN DE TRABAJO DEL EQUIPO — CHINOS CAFÉ S.A.

**Examen Parcial 2 · Ingeniería Web · UTP · Prof. Napoleón Ibarra**

| Integrante | Rol | Equipo | IP | Rama Git |
|---|---|---|---|---|
| **Daniel** | Servidor / Desarrollo / Víctima | Laptop A | `172.20.10.100` | `main` |
| **Edrian Hiraldo** (`Ashborn666`) | Red / Seguridad / Atacante | Laptop B (Kali) | `172.20.10.105` | `feature/laptop-b` |

**Red:** SSID `EXAMEN PARCIAL2` · `172.20.10.0/24` · Gateway `172.20.10.1` · DNS `172.20.10.1` / `8.8.8.8`
**Alcance:** exclusivamente la LAN aislada del examen. Sin Internet (Parte III).

> Regla de oro: **Laptop A es la única que reinicia servicios.** Laptop B monitorea, ataca y, si A cae, ejecuta el runbook por SSH. Nunca ambos a la vez.

---

## 0. Resumen de responsabilidades

| Área | Laptop A (Daniel) | Laptop B (Edrian) |
|---|---|---|
| App Flask / BD | Dueño del código y la BD principal | Valida réplica y coherencia de datos |
| NGINX / HTTPS | Aplica y mantiene la configuración | Verifica cabeceras y rate-limit desde fuera |
| Firewall / Knockd | Configura UFW y knockd | Ejecuta la secuencia de knocking y valida |
| Monitoreo | Ejecuta `agente_defensa.sh` | Paneles de monitoreo remoto + capturas |
| Ataques | Recibe y mitiga | Ejecuta `agente_ataque.sh` |
| Recuperación | Restaura servicio/BD | Cronometra y documenta la recuperación |
| Evidencias | Capturas del lado servidor | Capturas del lado atacante |
| Informe final | Parte I + despliegue | Partes II y III + consolidación |

---

## 1. Tareas de Laptop A — Daniel (Servidor / Víctima)

### 1.1 Preparación del servidor
- [ ] Confirmar SO real del servidor (Ubuntu Server VM o Windows) y documentarlo.
- [ ] Confirmar topología de ejecución: NGINX en `:8080/:8443` → Waitress en `127.0.0.1:8000`.
- [ ] Aplicar IP fija `172.20.10.100/24`, gateway `172.20.10.1`, DNS `172.20.10.1` + `8.8.8.8`.
- [ ] Verificar conectividad: `ping 172.20.10.1` y `ping 172.20.10.105`.
- [ ] Instalar dependencias: `python3-venv`, `nginx`, `ufw`, `knockd`, `fail2ban`, `openssl`.
- [ ] Confirmar que la app arranca: `systemctl status chinos`.

### 1.2 Hardening de NGINX
- [ ] Agregar `limit_req_zone` y `limit_conn_zone` en el bloque `http`.
- [ ] Aplicar `limit_req zone=chinos burst=10 nodelay` y `limit_conn chinos 20` en `location /`.
- [ ] Ajustar timeouts anti-Slowloris: `client_body_timeout`, `client_header_timeout`, `send_timeout` a `10s`.
- [ ] Limitar `client_max_body_size 2m`.
- [ ] Agregar cabeceras: `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Content-Security-Policy`.
- [ ] Validar con `sudo nginx -t` y recargar con `sudo systemctl reload nginx`.

### 1.3 Hardening del kernel (anti-DDoS)
- [ ] Activar SYN cookies: `net.ipv4.tcp_syncookies=1`.
- [ ] Subir `net.core.somaxconn=4096` y `net.ipv4.tcp_max_syn_backlog=4096`.
- [ ] Reducir `net.ipv4.tcp_fin_timeout=15` y `net.ipv4.tcp_keepalive_time=300`.
- [ ] Ampliar `net.ipv4.ip_local_port_range=1024 65000`.
- [ ] Anti-spoofing: `net.ipv4.conf.all.rp_filter=1`, `net.ipv4.tcp_synack_retries=2`, `net.ipv4.icmp_echo_ignore_broadcasts=1`.
- [ ] Aplicar con `sudo sysctl --system` y verificar con `sysctl net.ipv4.tcp_syncookies` (fichero plantilla: `scripts/servidor/sysctl_hardening.conf`).

### 1.4 Firewall y Port Knocking
- [ ] `ufw default deny incoming` / `allow outgoing`.
- [ ] Abrir solo `8080/tcp` y `8443/tcp`.
- [ ] Dejar `22/tcp` y `21/tcp` cerrados por defecto.
- [ ] Configurar `knockd`: SSH `7000,8000,9000` · FTP `7100,8100,9100`.
- [ ] Verificar que sin knocking `nmap` ve `22` y `21` como `filtered`.

### 1.5 Fail2ban
- [ ] Activar jail `sshd` (5 intentos / 10 min → ban 1 h).
- [ ] Activar jail `nginx-limit-req` (5 eventos / 1 min → ban 1 h).
- [ ] Activar jail `vsftpd` si el FTP está expuesto.
- [ ] `ignoreip` solo con `127.0.0.1/8` y `172.20.10.1` (gateway). **No incluir `172.20.10.105`**, de lo contrario Hydra no podrá ser baneado y la demo pierde sentido.

### 1.6 Agente de defensa
- [ ] Instalar `agente_defensa.sh` en `/usr/local/bin/`.
- [ ] Crear unidad `agente-defensa.service` con `Restart=always`.
- [ ] Verificar logs en `/var/log/chinos/defensa.jsonl`.
- [ ] Probar caída controlada: `systemctl stop chinos` → el agente debe levantarlo en < 60 s.

### 1.7 Respaldos y recuperación
- [ ] Tomar **snapshot de VirtualBox** con la app funcionando (estado "listo para examen").
- [ ] Programar `backup_db.sh` cada 5 min vía `cron`.
- [ ] Respaldar `/etc/nginx`, `/etc/knockd.conf` y `/etc/systemd/system/chinos.service` en `~/backup-config/`.
- [ ] Ensayar restauración de BD y medir el tiempo (objetivo: < 2 min).

### 1.8 Evidencias del lado servidor
- [ ] Captura de `ip a` con fecha/hora visible.
- [ ] Captura de `systemctl status chinos nginx knockd fail2ban`.
- [ ] Captura de `nginx -t` y del bloque de rate-limit.
- [ ] Captura de `ufw status numbered` antes y después del knocking.
- [ ] Captura de `fail2ban-client status` con IPs baneadas.
- [ ] Captura del dashboard/`htop` durante el ataque.
- [ ] Captura de la restauración tras la caída provocada.

---

## 2. Tareas de Laptop B — Edrian (Kali / Red / Ataque)

### 2.1 Preparación de Kali
- [ ] Confirmar adaptador en **Modo Puente (Bridged)** y IP `172.20.10.105/24`.
- [ ] Verificar salida a la LAN: `ping 172.20.10.100` y `ping 172.20.10.1`.
- [ ] Instalar/verificar herramientas:
  - `nmap`, `hydra`, `ab` (`apache2-utils`), `tcpdump`, `hping3`, `nethogs`, `iftop`, `knockd`, `wireshark`, `burpsuite`, `slowhttptest`.
- [ ] Crear `/root/auditoria_parcial2/` con `usuarios.txt`, `passwords.txt` y `evidencias/`.

### 2.2 Scripts de auditoría (versionados en el repo)
- [ ] `ejecutar_pruebas.sh`: menú interactivo con las 6 pruebas de la Parte III.
- [ ] Validación de alcance: rechazar cualquier IP fuera de `172.20.10.0/24`.
- [ ] Registrar `audit.log` con fecha, objetivo, comando y resultado.
- [ ] Guardar toda salida en `evidencias/<timestamp>_<prueba>.txt`.
- [ ] Subir los scripts a `feature/laptop-b` (hoy solo viven en la VM).

### 2.3 Pruebas de ataque (solo con autorización del profesor)
- [ ] **1. Nmap pre-knocking:** `nmap -sS -Pn -p 21,22,80,8080,8443 172.20.10.100` → debe salir `filtered`.
- [ ] **2. Port Knocking:** `knock 172.20.10.100 7000 8000 9000` → verificar apertura de `22`.
- [ ] **3. Nmap post-knocking:** repetir y comparar resultados.
- [ ] **4. Hydra:** `hydra -L usuarios.txt -P passwords.txt ssh://172.20.10.100` y variante FTP.
- [ ] **5. Saturación:** `ab -n 20000 -c 500 http://172.20.10.100:8080/` → medir RPS y errores.
- [ ] **6. Cabeceras:** `curl -I http://172.20.10.100:8080` vs `curl -kI https://172.20.10.100:8443` → comparar.
- [ ] **7. Captura:** `tcpdump -i eth0 -w evidencias/<ts>_ataque.pcap host 172.20.10.100`.

### 2.4 Monitoreo remoto
- [ ] Mantener una terminal con `watch -n 2 'ss -s'`.
- [ ] Mantener una terminal con `watch -n 2 'ss -tn state established | awk "{print \$5}" | cut -d: -f1 | sort | uniq -c | sort -rn | head'`.
- [ ] Seguir en vivo `tail -f /var/log/nginx/access.log` por SSH.
- [ ] Tener `iftop` o `nethogs` abierto durante el ataque.

### 2.5 Soporte y recuperación
- [ ] Tener acceso SSH probado **con knocking previo**.
- [ ] Cronometrar la recuperación cuando A reinicie el servicio.
- [ ] Si A no responde: verificar réplica Supabase y `http://172.20.20.100` en Packet Tracer.
- [ ] Documentar el tiempo de caída (MTTR) para el informe.

### 2.6 Evidencias del lado atacante
- [ ] Captura de `ip a` en Kali con fecha/hora.
- [ ] Captura de Nmap antes y después del knocking.
- [ ] Captura de la secuencia de knocking y del `ufw` resultante.
- [ ] Captura de Hydra (intentos fallidos + ban de fail2ban).
- [ ] Captura de `ab` con RPS y tasa de errores (antes/después de `limit_req`).
- [ ] Captura de `curl -I` HTTP vs HTTPS.
- [ ] Captura de Wireshark/tcpdump con el tráfico del ataque.

---

## 3. Tareas compartidas (las hacen juntos)

- [ ] **Ensayo general** en la LAN real, con ambos equipos conectados al SSID `EXAMEN PARCIAL2`.
- [ ] **Línea base:** medir el sistema sin mitigación (RPS, latencia, errores) antes de aplicar `limit_req`.
- [ ] **Comparativa:** repetir las mismas pruebas con mitigación y tabular resultados.
- [ ] **Prueba de caída controlada:** A detiene el servicio, se mide el tiempo de recuperación del agente.
- [ ] **Verificación de réplica:** crear pedido y pago en A, confirmar el registro en Supabase desde B.
- [ ] **Checklist de capturas:** 3 momentos por prueba (Inicio / Proceso / Resultado) con fecha y hora del sistema visibles.
- [ ] **Reglas de enfrentamiento** acordadas y firmadas por ambos (ver sección 6).
- [ ] **Commit final** en `feature/laptop-b` y Pull Request a `main`.

---

## 4. Cronograma

| Cuándo | Laptop A (Daniel) | Laptop B (Edrian) |
|---|---|---|
| **D-5 / D-4** | Hardening NGINX, sysctl, fail2ban, backups | Escribir y probar `agente_ataque.sh` + diccionarios |
| **D-3** | Instalar `agente_defensa.sh` y probar caída | Ensayo de fuego: `ab`, `hydra`, `nmap` |
| **D-2** | Calibrar umbrales, ensayar restauración | Tabular resultados, ajustar playbook |
| **D-1** | Snapshot final, no tocar configuración | Cargar herramientas, checklist de evidencias |
| **Día D** | Ejecutar runbook y monitorear | Atacar, monitorear y capturar |

---

## 5. Runbook "si el sistema cae" (ambos deben saberlo)

| Escenario | Detección | Acción | Responsable |
|---|---|---|---|
| Flask caído | `curl` falla 3 veces | `sudo systemctl restart chinos` | A (o B por SSH) |
| NGINX saturado | 502/504 masivos | `sudo systemctl reload nginx` + revisar `limit_req` | A |
| Disco lleno | `df -h` > 90 % | `sudo truncate -s 0 /var/log/nginx/access.log` | A |
| BD corrupta | La app no lista pedidos | `cp ~/backup-db/chinos_cafe_<hora>.db chinos_cafe.db && restart` | A |
| Servidor irrecuperable | SSH no responde | Mostrar continuidad de servicio en Supabase (réplica cloud). El sitio `172.20.20.100` existe solo en Packet Tracer (Veraguas) y se usa únicamente como narrativa de la Parte II. | B propone, A ejecuta |
| VM comprometida | Procesos anómalos | Restaurar snapshot de VirtualBox | A |

**Objetivo de recuperación (RTO): menos de 2 minutos.**

---

## 6. Reglas de enfrentamiento

1. Solo se ataca lo que el profesor autorice explícitamente.
2. Nada fuera del rango `172.20.10.0/24`.
3. No se ataca el gateway `172.20.10.1` ni equipos de infraestructura del aula.
4. No se borran datos ni se instala persistencia en equipos rivales.
5. Ante la señal de "stop" del profesor, se detiene todo y se documenta.
6. Toda acción ofensiva queda registrada en `audit.log` con fecha, hora y objetivo.

---

## 7. Definición de "terminado"

- [ ] El servidor resiste `ab -n 20000 -c 500` sin caer: ≥ 95 % de respuestas 2xx/3xx y el resto como 503 por rate-limit (no como timeouts).
- [ ] El servidor se recupera solo en menos de 60 s tras una caída del servicio.
- [ ] Hydra no obtiene credenciales y fail2ban banea la IP atacante.
- [ ] Los puertos 21 y 22 están cerrados sin knocking.
- [ ] La réplica en Supabase refleja pedidos y pagos en tiempo real.
- [ ] Existen 3 capturas con fecha/hora por cada prueba.
- [ ] El informe final está consolidado y el PR está aprobado.

---

*Documento vivo: actualizar el estado de las casillas a medida que avancen.*
