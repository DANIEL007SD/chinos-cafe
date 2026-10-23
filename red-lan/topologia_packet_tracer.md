# Guía de Construcción: Topología de Red en Cisco Packet Tracer

Esta guía detalla la configuración exacta para recrear el escenario de red del **Examen Parcial 2** en **Cisco Packet Tracer** cumpliendo con los parámetros indicados por el profesor: conexión Ethernet al router, SSID `EXAMENPARCIAL2` y clave `1234567890`.

---

## 1. Dispositivos a Colocar en el Área de Trabajo

| Dispositivo en Packet Tracer | Nombre del Dispositivo | Conexión Física | Dirección IP / Rol |
| :--- | :--- | :--- | :--- |
| **Wireless Router (ej. WRT300N)** | `ROUTER-EXAMEN-PARCIAL2` | Central | `172.20.10.1` (Gateway / DHCP) |
| **Server-PT** | `SRV-CHINOS-WEB` | Cable directo Ethernet a puerto Ethernet 1 del router | `172.20.10.100` (Servidor NGINX / Flask) |
| **PC-PT (o Laptop)** | `KALI-LINUX-ATACANTE` | Cable directo Ethernet a puerto Ethernet 2 del router | `172.20.10.105` (Atacante / Auditoría) |
| **Laptop-PT** | `LAPTOP-A-DEV` | Cable directo a Ethernet 3 o conexión Wi-Fi | `172.20.10.101` (Host Laptop A) |
| **Laptop-PT** | `LAPTOP-B-ADMIN` | Cable directo a Ethernet 4 o conexión Wi-Fi | `172.20.10.102` (Host Laptop B) |
| **Cloud-PT (Nube / Internet)** | `SUPABASE-CLOUD` | Conectado al puerto Internet (WAN) del router | `talewwtbjoyfsoresvmx.supabase.co` |

---

## 2. Configuración del Router en Packet Tracer

1. Haz clic en el **Wireless Router** ➔ pestaña **GUI**:
2. **Setup ➔ Basic Setup:**
   * **IP Address:** `172.20.10.1`
   * **Subnet Mask:** `255.255.255.0`
   * **DHCP Server:** `Enabled`
   * **Start IP Address:** `172.20.10.100`
   * **Maximum number of Users:** `50`
   * **Static DNS 1:** `172.20.10.1`
   * Clic en **Save Settings** (al fondo de la página).
3. **Wireless ➔ Basic Wireless Settings:**
   * **Network Name (SSID):** `EXAMENPARCIAL2`
   * Clic en **Save Settings**.
4. **Wireless ➔ Wireless Security:**
   * **Security Mode:** `WPA2 Personal`
   * **Encryption:** `AES`
   * **Passphrase:** `1234567890`
   * Clic en **Save Settings**.

---

## 3. Configuración de los Equipos en Packet Tracer

### Servidor Web (`SRV-CHINOS-WEB`):
1. **Desktop ➔ IP Configuration:**
   * **IP Address:** `172.20.10.100`
   * **Subnet Mask:** `255.255.255.0`
   * **Default Gateway:** `172.20.10.1`
   * **DNS Server:** `172.20.10.1`
2. **Config ➔ Services ➔ HTTP:**
   * Asegúrate de que **HTTP** y **HTTPS** estén en **ON**.
   * Edita `index.html` para simular la app de Chinos Café:
     ```html
     <h3>CHINOS CAFE S.A. - Servidor Web</h3>
     <p>IP: 172.20.10.100 | HTTP: 8080 | HTTPS: 8443</p>
     ```

### Máquina Atacante Kali (`KALI-LINUX-ATACANTE`):
1. **Desktop ➔ IP Configuration:**
   * Elige **DHCP** (deberá recibir una IP en el rango `172.20.10.10x`) o configúrala estática con `172.20.10.105`.
   * **Default Gateway:** `172.20.10.1`

---

## 4. Pruebas de Validación dentro de Packet Tracer

1. **Prueba ICMP (Ping):**
   * Desde `KALI-LINUX-ATACANTE` ➔ **Desktop** ➔ **Command Prompt**:
     ```
     ping 172.20.10.100
     ```
     *Debe responder 4 paquetes exitosos.*
2. **Prueba Web Browser:**
   * Desde `KALI-LINUX-ATACANTE` ➔ **Desktop** ➔ **Web Browser**:
   * Escribe: `http://172.20.10.100` y pulsa **Go**.
   * Debe desplegar la página de Chinos Café.
3. **Captura:**
   * Toma una captura de pantalla del diagrama completo con las luces verdes de enlace y del ping exitoso para el informe.

---

## 5. Guardar Archivo
Guarda el archivo en esta carpeta con el nombre:
`red-lan/topologia_red_parcial2.pkt`
