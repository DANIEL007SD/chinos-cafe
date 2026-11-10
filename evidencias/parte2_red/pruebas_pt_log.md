# Pruebas Packet Tracer — Parcial2.pkt

**Fecha:** 2026-11-10 12:11–12:15 (reloj del sistema visible en capturas)
**Archivo:** `red-lan/Parcial2.pkt` (md5: `d9562b739e57dd25862a06cfa86171bf`)
**Equipo probado:** Laptop `LCH01` (IP `172.20.10.101`, gateway VIP HSRP `172.20.10.1`)

## Capturas en 3 momentos
| Momento | Archivo | Qué prueba |
|---|---|---|
| **Inicio** | `20261110_1211_pt_topologia_cargada_INICIO.jpg` | Topología cargada, enlaces convergidos (verdes). Visible: Dual-AP Chiriquí (Ch1+Ch6), WLAN Veraguas Ch11, Núcleo HSRP v2 (R1 + R2-Secundario), EtherChannel LACP Po1 (SW0 ↔ SW0-BKP), Sucursal Veraguas con SW1 y SO2. |
| **Proceso** | `20261110_1214_pt_ping_vip_y_so1_PROCESO.jpg` | `ipconfig` de LCH01 (IPv4 172.20.10.101, GW 172.20.10.1) + `ping 172.20.10.1` (VIP HSRP) **4/4 replies, 0% loss, TTL=255** + `ping 172.20.10.100` (SO1 Flask) **4/4 replies, 0% loss, TTL=128**. |
| **Resultado** | `20261110_1215_pt_ping_cross_site_RESULTADO.jpg` | `ping 172.20.20.100` (SO2 Veraguas) desde Chiriquí: **3/4 replies, 25% loss, TTL=127**. El primer paquete pierde por ARP inicial (normal en PT); TTL=127 confirma que atravesó 1 router → ruteo inter-sitio OK. |

## Qué se demuestra
1. **Capa 3 HSRP operativa:** la laptop responde al VIP `172.20.10.1`, no a una IP física de router.
2. **Capa 7 (servidor):** SO1 responde en `172.20.10.100` desde la LAN de Chiriquí.
3. **Ruteo inter-sitio:** LCH01 (Chiriquí) alcanza SO2 (Veraguas) a través del backbone HSRP.
4. **Convergencia de la topología:** sin apagar nada, el tráfico fluye en ambas sedes.

## Pruebas pendientes (requieren acciones manuales)
- **Failover HSRP:** apagar R1, repetir `ping 172.20.10.1`; debe seguir respondiendo (R2-Secundario toma el VIP).
- **Failover LACP:** desconectar un enlace del Port-channel 1, verificar que el ping SW0↔SW0-BKP sigue.
- **Failover Dual-AP:** apagar AP-CH1, verificar que la Tablet se reasocia a AP-CH2-BKP.
- **Navegación web embebida:** desde LCH01 → `http://172.20.10.100` (Server SO1) para mostrar las 4 páginas del prototipo.

> Estas 4 pruebas se harán en vivo frente al profesor durante la sustentación, con capturas Inicio/Proceso/Resultado para cada una.
