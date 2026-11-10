# Demos en vivo de Packet Tracer — Parte II

**Fecha:** 2026-11-10 ~14:54–14:59 (reloj del sistema visible en capturas)
**Archivo:** `red-lan/Parcial2.pkt`

## Demo 1 — Navegación web embebida (Punto 4 del examen)
Desde LCH01 (Desktop → Web Browser) se navegó el prototipo alojado en SO1 (`172.20.10.100`).
- `20261110_1454_pt_web_index_INICIO.jpg` — página **Inicio** de CHINOS CAFE S.A. con menú Inicio / Fábrica / Pedidos / Pagos.
- `20261110_1454_pt_web_fabrica_RESULTADO.jpg` — página **Fábrica (CRUD Pizzas)** cargada tras hacer click en el menú → navegación interna funcional.
- **Demuestra:** el servidor web embebido responde HTTP y las 4 páginas son navegables en simulación.

## Demo 2 — EtherChannel LACP (Capa 2, redundancia de enlace)
En SW0 (`show etherchannel summary`), corte de un enlace del Port-channel.
- `20261110_1455_pt_lacp_2enlaces_INICIO.jpg` — `Po1(SU)` LACP con **ambos** puertos `Fa0/23(P) Fa0/24(P)` bundled.
- `20261110_1456_pt_lacp_1enlace_RESULTADO.jpg` — tras `shutdown` de Fa0/23: `Po1(SU)` **sigue operativo** con `Fa0/23(D)` down y `Fa0/24(P)` activo.
- **Demuestra:** el EtherChannel sobrevive la caída de un enlace físico; el tráfico continúa por el enlace restante. (Fa0/23 restaurado con `no shutdown` después.)

## Demo 3 — Redundancia Dual-AP (Capa 1/2 inalámbrica, roaming)
Ping continuo `ping -t 172.20.10.1` desde Tablet-CH mientras se apaga AP-CH1 (Port 1 radio → Off).
- `20261110_1458_pt_dualAP_roaming_RESULTADO.jpg` — el ping **sigue respondiendo** (TTL=255 ininterrumpido) tras apagar AP-CH1: la Tablet se reasoció a **AP-CH2-BKP** (Canal 6) sin perder conectividad.
- **Demuestra:** con el mismo SSID `EXAMEN PARCIAL2` en ambos AP, el cliente hace roaming automático al AP de respaldo. (AP-CH1 reactivado después.)

## Estado Parte II: COMPLETA
Las 4 demostraciones clave quedan evidenciadas:
1. ✓ Failover HSRP (apagado de R1) — ver `hsrp_fix_log.md` + capturas previas.
2. ✓ EtherChannel LACP (Demo 2).
3. ✓ Dual-AP roaming (Demo 3).
4. ✓ Navegación web embebida (Demo 1).

Pendiente solo para la sustentación en vivo: repetir con capturas Inicio/Proceso/Resultado si el profesor lo exige en los 3 momentos por prueba.
