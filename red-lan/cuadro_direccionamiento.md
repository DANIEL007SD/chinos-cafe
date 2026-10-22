# Parte II: Cuadro de Direccionamiento IP y Especificación de Red

## 1. Parámetros Generales de la Red LAN Inalámbrica

* **Nombre de Red (SSID):** `EXAMEN PARCIAL2`
* **Tipo de Red:** LAN Inalámbrica 802.11n/ac (WLAN)
* **Seguridad:** WPA2-Personal (AES)
* **Dirección de Red:** `172.20.10.0/24`
* **Máscara de Subred:** `255.255.255.0`
* **Puerta de Enlace Predeterminada (Gateway):** `172.20.10.1`
* **Rango de Asignación DHCP:** `172.20.10.100` – `172.20.10.199`
* **DNS:** `172.20.10.1` / `8.8.8.8`

---

## 2. Cuadro Maestro de Direccionamiento IP (Alineado con `DEPLOY.md`)

| Dispositivo | Nombre de Host | Interfaz | Tipo de IP | Dirección IP | Máscara | Gateway | Servicios y Puertos | Rol en la Arquitectura |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Router / Hotspot** | `GW-ROUTER-01` | WLAN / Gi0/0 | Estática | `172.20.10.1` | `255.255.255.0` | N/A | DHCP, DNS, NAT | Puerta de enlace y punto de acceso del SSID `EXAMEN PARCIAL2` |
| **VM Servidor Web (Laptop A)** | `SRV-CHINOS-WEB` | `enp0s3` (Puente) | Estática (`netplan`) | `172.20.10.100` | `255.255.255.0` | `172.20.10.1` | **8080 (HTTP), 8443 (HTTPS), 22 (SSH + Knockd), 21 (FTP + Knockd)** | Servidor principal de la app Flask + NGINX + SQLite local |
| **Laptop A (Física)** | `LAPTOP-A-HOST` | Wi-Fi 802.11 | DHCP | `172.20.10.101` | `255.255.255.0` | `172.20.10.1` | Cliente Web / SSH | Equipo anfitrión de desarrollo (Laptop A) |
| **Laptop B (Física)** | `LAPTOP-B-HOST` | Wi-Fi 802.11 | DHCP | `172.20.10.102` | `255.255.255.0` | `172.20.10.1` | Packet Tracer / Dashboard Supabase | Equipo anfitrión de red y monitoreo de réplica (Laptop B) |
| **VM Kali Linux (Laptop B)** | `VM-KALI-AUDIT` | `eth0` (Puente) | DHCP / Estática | `172.20.10.105` | `255.255.255.0` | `172.20.10.1` | Herramientas de diagnóstico de red | Máquina virtual de verificación de red y pruebas |
| **BD Réplica (Supabase)** | `SUPABASE-CLOUD` | HTTPS / TLS | Cloud | `<project-ref>.supabase.co` | N/A | Internet / NAT | **443 (REST PostgREST) / 5432 (PostgreSQL)** | Segunda base de datos relacional (`pedido_replica`, `pago_replica`) |
