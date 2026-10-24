# Parte II: Cuadro Maestro de Direccionamiento IP y Arquitectura Redundante

## 1. Parámetros Oficiales de Red y Alta Disponibilidad

* **Subred LAN Laboratorio:** `172.20.10.0/24` (Máscara `255.255.255.0`)
* **Puerta de Enlace Virtual (VIP HSRP Grupo 10):** `172.20.10.1`
* **Rango DHCP Redundante (Split-Scope `172.20.10.100–199`):**
  * Sub-rango Estático reservado (Servidores y VMs): `172.20.10.100` – `172.20.10.109`
  * Pool DHCP Primario (`R1-PRINCIPAL`): `172.20.10.110` – `172.20.10.149`
  * Pool DHCP Respaldo (`R2-RESPALDO`): `172.20.10.150` – `172.20.10.199`
* **Red Inalámbrica (Roaming Dual-AP):**
  * **SSID:** `EXAMENPARCIAL2`
  * **Seguridad:** WPA2-PSK (AES) · **Clave:** `1234567890`
  * **Canales sin solapamiento:** Canal `1` (`AP1`) y Canal `6` (`AP2`)
* **Subred WAN / Cloud (Simulación Supabase):** `203.0.113.0/24` (NAT Overload en `R1` y `R2`)

---

## 2. Cuadro Maestro de Direccionamiento IP

| Dispositivo | Nombre de Host | Interfaz | Modo | Dirección IP | Máscara | Gateway | Rol y Mecanismo de Redundancia |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Gateway Virtual** | `VIP-HSRP-G10` | Virtual (Capa 3) | HSRP v2 | **`172.20.10.1`** | `255.255.255.0` | N/A | IP flotante compartida entre `R1` y `R2` |
| **Router Primario** | `R1-PRINCIPAL` | `Gig0/0` (LAN)<br>`Gig0/1` (WAN) | Estática | `172.20.10.2`<br>`203.0.113.2` | `255.255.255.0`<br>`255.255.255.0` | N/A | **HSRP Active** (Prioridad 110 + Preempt), DHCP `.110–.149`, NAT |
| **Router Respaldo** | `R2-RESPALDO` | `Gig0/0` (LAN)<br>`Gig0/1` (WAN) | Estática | `172.20.10.3`<br>`203.0.113.3` | `255.255.255.0`<br>`255.255.255.0` | N/A | **HSRP Standby** (Prioridad 100), DHCP `.150–.199`, NAT Backup |
| **Switch Primario** | `SW1-CORE` | `VLAN 1` + `Po1` | Estática | `172.20.10.11` | `255.255.255.0` | `172.20.10.1` | **STP Root Primary** + EtherChannel LACP (`Fa0/23-24`) |
| **Switch Secundario** | `SW2-REDUNDANTE` | `VLAN 1` + `Po1` | Estática | `172.20.10.12` | `255.255.255.0` | `172.20.10.1` | **STP Root Secondary** + EtherChannel LACP (`Fa0/23-24`) |
| **Access Point 1** | `AP1-WIFI-CH1` | `Port 0` / WLAN | Puente L2 | N/A (Capa 2) | N/A | N/A | SSID `EXAMENPARCIAL2` (Canal 1, WPA2 `1234567890`) |
| **Access Point 2** | `AP2-WIFI-CH6` | `Port 0` / WLAN | Puente L2 | N/A (Capa 2) | N/A | N/A | SSID `EXAMENPARCIAL2` (Canal 6, Roaming de respaldo) |
| **VM Servidor Web** | `SRV-CHINOS-WEB` | `Fa0` / `enp0s3` | Estática | **`172.20.10.100`** | `255.255.255.0` | `172.20.10.1` | **Servidor Primario:** NGINX + Flask (8080/8443), SSH/FTP Knockd, DNS |
| **Laptop A (Física)** | `LAPTOP-A-DEV` | Ethernet `Fa0` | Estática | `172.20.10.101` | `255.255.255.0` | `172.20.10.1` | Host de desarrollo y monitoreo (Laptop A) |
| **Laptop B (Física)** | `LAPTOP-B-ADMIN` | Ethernet `Fa0` | Estática | `172.20.10.102` | `255.255.255.0` | `172.20.10.1` | Host de red, Packet Tracer y panel Supabase (Laptop B) |
| **VM Kali Linux** | `VM-KALI-LINUX` | `Fa0` / `eth0` | Estática | **`172.20.10.105`** | `255.255.255.0` | `172.20.10.1` | Estación de auditoría de seguridad (Nmap, Wireshark, Knock) |
| **Clientes Wi-Fi** | `CELULAR-YAPPY` / `CLIENTE-WIFI` / `TABLET-WIFI` | `Wireless0` | DHCP | `172.20.10.110+` | `255.255.255.0` | `172.20.10.1` | Clientes móviles en roaming sobre `EXAMENPARCIAL2` |
| **BD Réplica Cloud** | `SRV-SUPABASE-REPLICA` | `Fa0` (WAN) | Estática | **`203.0.113.10`** | `255.255.255.0` | `203.0.113.1` | **Réplica Relacional:** Simulación de `talewwtbjoyfsoresvmx.supabase.co` |
