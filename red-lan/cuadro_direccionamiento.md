# Parte II: Cuadro Maestro de Direccionamiento IP y Especificación de Red

## 1. Parámetros Oficiales del Router de Laboratorio

* **Topología de Conexión:** Híbrida (Conexión por cable Ethernet a los puertos LAN del Router + Cobertura WLAN).
* **Nombre de Red Inalámbrica (SSID):** `EXAMENPARCIAL2`
* **Contraseña Wi-Fi (Pre-Shared Key):** `1234567890`
* **Seguridad Inalámbrica:** WPA2-Personal (Cifrado AES)
* **Dirección de Red:** `172.20.10.0/24`
* **Máscara de Subred:** `255.255.255.0` (`/24`)
* **Puerta de Enlace Predeterminada (Gateway):** `172.20.10.1`
* **Rango del Pool DHCP:** `172.20.10.100` – `172.20.10.199`
* **Servidores DNS:** `172.20.10.1` / `8.8.8.8`

---

## 2. Cuadro Maestro de Direccionamiento IP (Examen Parcial 2)

| Dispositivo / Equipo | Nombre de Host | Interfaz Física / Lógica | Modo IP | Dirección IP | Máscara de Subred | Puerta de Enlace | Servicios y Puertos Clave | Rol en el Escenario |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Router de Laboratorio** | `ROUTER-CISCO-01` | FastEthernet / Gi0/0 + WLAN | Estática | `172.20.10.1` | `255.255.255.0` | N/A | DHCP Server, DNS Relay, Gateway | Emite SSID `EXAMENPARCIAL2`, distribuye puertos Ethernet y conmuta tráfico LAN |
| **VM Servidor Web (Laptop A)** | `SRV-CHINOS-WEB` | `enp0s3` (Adaptador Puente) | Estática (`netplan`) | `172.20.10.100` | `255.255.255.0` | `172.20.10.1` | **8080/tcp** (HTTP)<br>**8443/tcp** (HTTPS SSL)<br>**22/tcp** (SSH + Knockd)<br>**21/tcp** (FTP + Knockd) | **Servidor Objetivo / Mitigación:** Aloja la app Flask con proxy NGINX, SQLite local y firewall UFW |
| **Laptop A (Host Físico)** | `LAPTOP-A-DEV` | Ethernet RJ45 / Wi-Fi | DHCP | `172.20.10.101` | `255.255.255.0` | `172.20.10.1` | Navegador Web, Cliente SSH | Equipo anfitrión del desarrollador (Laptop A) |
| **Laptop B (Host Físico - Tú)**| `LAPTOP-B-ADMIN` | Ethernet RJ45 (`Realtek USB GbE`) | DHCP | `172.20.10.102` | `255.255.255.0` | `172.20.10.1` | Packet Tracer, Dashboard Supabase | Equipo anfitrión de red, gestión de réplica y atacante (Laptop B) |
| **VM Kali Linux (Laptop B)** | `KALI-LINUX-ATK`| `eth0` (Adaptador Puente) | DHCP / Estática | `172.20.10.105` | `255.255.255.0` | `172.20.10.1` | Nmap, Wireshark, Knock, Curl | **Máquina Atacante / Auditoría:** Lanza el escaneo de puertos, análisis de tráfico y pruebas de seguridad |
| **BD Réplica Cloud (Supabase)** | `SUPABASE-CLOUD` | HTTPS (TLS 1.3) | Cloud | `talewwtbjoyfsoresvmx.supabase.co` | N/A | Internet / NAT | **443/tcp** (PostgREST API)<br>**5432/tcp** (PostgreSQL) | **Segunda Base de Datos:** Réplica relacional en la nube de `pedido_replica` y `pago_replica` |

---

## 3. Configuración de Interfaces de Red Físicas

### Para Laptop B (Tu Laptop):
* **Si te conectas por cable de red (Ethernet recomendado por el profesor):**
  Tu laptop tiene el adaptador **`Realtek USB GbE Family Controller`**.
  En VirtualBox, la VM de Kali Linux se puentea a ese adaptador.
* **Si te conectas por Wi-Fi:**
  Te asocias al SSID `EXAMENPARCIAL2` con la clave `1234567890`. Tu tarjeta es **`Realtek 8821CE Wireless LAN 802.11ac PCI-E NIC`**.

---

## 4. Secuencia de Verificación de Conectividad (Pre-Ataque)

Desde la terminal de tu **Kali Linux**:

```bash
# 1. Comprobar que Kali recibió IP en el rango 172.20.10.x
ip a

# 2. Ping al Router (Gateway)
ping -c 3 172.20.10.1

# 3. Ping al Servidor de Laptop A
ping -c 3 172.20.10.100

# 4. Verificar que la app web de Laptop A responda
curl -I http://172.20.10.100:8080
```
