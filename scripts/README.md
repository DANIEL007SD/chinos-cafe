# Scripts del equipo — CHINOS CAFÉ S.A.

Scripts versionados en Git para que el día del examen cualquier integrante pueda
restaurarlos aunque la VM principal falle.

## `kali/` — Laptop B (atacante)
| Archivo | Descripción |
|---|---|
| `ejecutar_pruebas.sh` | Menú interactivo con las 6+1 pruebas de la Parte III (nmap, knock, hydra, ab, curl, tcpdump). Valida alcance a `172.20.10.0/24` y registra todo en `audit.log`. |

Se instala en Kali en `~/auditoria_parcial2/ejecutar_pruebas.sh` y requiere los
diccionarios `usuarios.txt` y `passwords.txt` en la misma carpeta.

## `servidor/` — Laptop A (víctima)
| Archivo | Descripción |
|---|---|
| `agente_defensa.sh` | Loop en Bash que verifica el servicio Flask, detecta ráfagas HTTP y bruteforce SSH; escribe JSONL en `/var/log/chinos/defensa.jsonl`. |
| `agente-defensa.service` | Unidad systemd con `Restart=always`. |
| `backup_db.sh` | Snapshot SQLite cada 5 min vía cron, con rotación de 24 h. |
| `nginx_hardening.conf` | Plantilla con `limit_req`, cabeceras de seguridad y timeouts anti-Slowloris. |
| `sysctl_hardening.conf` | Hardening de kernel (SYN cookies, rp_filter, somaxconn, etc.). |

## Instalación rápida en el servidor
```bash
sudo cp scripts/servidor/agente_defensa.sh /usr/local/bin/
sudo cp scripts/servidor/backup_db.sh      /usr/local/bin/
sudo cp scripts/servidor/agente-defensa.service /etc/systemd/system/
sudo cp scripts/servidor/sysctl_hardening.conf  /etc/sysctl.d/99-chinos.conf
sudo chmod +x /usr/local/bin/agente_defensa.sh /usr/local/bin/backup_db.sh
sudo systemctl daemon-reload
sudo systemctl enable --now agente-defensa.service
sudo sysctl --system
```

> Revisar las secciones comentadas de `nginx_hardening.conf` antes de aplicarlas
> a la configuración real de NGINX; el archivo es una guía, no se incluye tal cual.
