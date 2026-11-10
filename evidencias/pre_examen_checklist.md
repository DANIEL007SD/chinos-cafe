===== CHECKLIST PRE-EXAMEN â€” 2026-11-10 12:07:20 =====

## 1. Estructura del repo

total 171
drwxr-xr-x 1 willi 197609     0 Nov 10 12:07 .
drwxr-xr-x 1 willi 197609     0 Oct 22 09:36 ..
drwxr-xr-x 1 willi 197609     0 Nov  9 16:45 .claude
-rw-r--r-- 1 willi 197609   375 Oct 22 10:50 .env
-rw-r--r-- 1 willi 197609   905 Oct 22 10:03 .env.example
drwxr-xr-x 1 willi 197609     0 Nov 10 12:05 .git
-rw-r--r-- 1 willi 197609   219 Oct 22 10:00 .gitignore
-rw-r--r-- 1 willi 197609  6649 Oct 22 10:00 DEPLOY.md
-rw-r--r-- 1 willi 197609 11363 Nov 10 12:07 PLAN_EQUIPO.md
-rw-r--r-- 1 willi 197609  3001 Oct 22 10:00 README.md
drwxr-xr-x 1 willi 197609     0 Nov  9 17:20 __pycache__
-rw-r--r-- 1 willi 197609  8979 Oct 22 10:56 app.py
-rw-r--r-- 1 willi 197609 40960 Oct 22 10:59 chinos_cafe.db
-rw-r--r-- 1 willi 197609 12288 Oct 24 15:48 chinos_cafe_replica.db
drwxr-xr-x 1 willi 197609     0 Oct 22 10:59 comprobantes
-rw-r--r-- 1 willi 197609  2651 Oct 22 10:14 config.py
drwxr-xr-x 1 willi 197609     0 Oct 22 10:04 db-replica
drwxr-xr-x 1 willi 197609     0 Nov 10 12:07 evidencias
-rw-r--r-- 1 willi 197609  3727 Oct 22 10:00 models.py
drwxr-xr-x 1 willi 197609     0 Nov 10 12:03 red-lan
-rw-r--r-- 1 willi 197609  6632 Oct 22 10:02 replication.py
-rw-r--r-- 1 willi 197609    39 Oct 22 10:00 requirements.txt
drwxr-xr-x 1 willi 197609     0 Nov 10 12:06 scripts
-rw-r--r-- 1 willi 197609  1685 Oct 22 10:00 seed.py
drwxr-xr-x 1 willi 197609     0 Oct 22 10:00 static
drwxr-xr-x 1 willi 197609     0 Oct 22 10:00 templates
-rw-r--r-- 1 willi 197609 14916 Oct 22 10:55 utils.py

## 2. Rama y Ãºltimo commit

feature/laptop-b
12b3ba2 fix(red-lan): alinear Parcial2.pkt 100% con Figura 1 del PDF oficial y prototipo web embebido
19dde18 feat(red-lan): generar topologia empresarial redundante completa en Packet Tracer 9.0.1
1f478b2 docs(red-lan): topologia redundante HSRP + EtherChannel LACP + Dual AP en Packet Tracer

## 3. Archivo .pkt oficial

-rw-r--r-- 1 willi 197609 87148 Nov  9 17:41 red-lan/Parcial2.pkt
d9562b739e57dd25862a06cfa86171bf *red-lan/Parcial2.pkt

## 4. Scripts versionados

-rwxr-xr-x 1 willi 197609 3062 Nov 10 12:05 scripts/kali/ejecutar_pruebas.sh
-rw-r--r-- 1 willi 197609 1826 Nov 10 12:06 scripts/README.md
-rw-r--r-- 1 willi 197609 262 Nov 10 12:06 scripts/servidor/agente-defensa.service
-rwxr-xr-x 1 willi 197609 2055 Nov 10 12:06 scripts/servidor/agente_defensa.sh
-rwxr-xr-x 1 willi 197609 924 Nov 10 12:06 scripts/servidor/backup_db.sh
-rw-r--r-- 1 willi 197609 1333 Nov 10 12:06 scripts/servidor/nginx_hardening.conf
-rw-r--r-- 1 willi 197609 712 Nov 10 12:06 scripts/servidor/sysctl_hardening.conf

## 5. Config de Flask verificada

DB principal: sqlite:///C:\Users\willi\OneDrive\Documentos\Trabajos Universidad\Ingeniería Web\Parcial 2\chinos_cafe.db
DB replica: sqlite:///C:\Users\willi\OneDrive\Documentos\Trabajos Universidad\Ingeniería Web\Parcial 2\chinos_cafe_replica.db
Supabase URL ok: True
