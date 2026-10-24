# II PARTE: Simulación de RED LAN Inalámbrica y Cuadro de Direccionamiento IP

## 1. Cuadro Oficial de Configuración Física / Simulada (Punto 1 del Examen)

| CARACTERÍSTICAS (DHCP — RED LAN INALÁMBRICA) | SU IP DEL SERVIDOR (`SO1 LINUX BD1 / INTERFAZ WEB`) |
| :--- | :--- |
| **Modo:** DHCP (`Split-Scope` Redundante HSRP) | **Modo:** **IP FIJO** |
| **SSID:** `EXAMEN PARCIAL2` *(con espacio)* | **IP:** `172.20.10.100` *(Ej. NGINX `http://172.20.10.100:8080` y HTTPS)* |
| **IP (Rango):** `172.20.10.100 - 199` | **MR:** `255.255.255.0` |
| **MR:** `255.255.255.0` | **PE:** `172.20.10.1` *(Gateway Virtual HSRP Grupo 10)* |
| **PE:** `172.20.10.1` | **DNS1:** `172.20.10.1` |
| **DNS1:** `172.20.10.1` | **DNS2:** `8.8.8.8` |
| **DNS2:** `8.8.8.8` | **Seguridad SSH/FTP:** Port Knocking (`knockd`) + HTTPS NGINX |

> **Nota sobre distribución del rango `172.20.10.100 - 199`:**
> * **`172.20.10.100 - 172.20.10.109`:** Sub-rango excluido en DHCP para asignaciones estáticas críticas (`SO1` `.100`, `LCH01` `.101`, `LCH02-LAPTOP-B` `.102`, `VM-KALI-LINUX` `.105`).
> * **`172.20.10.110 - 172.20.10.149`:** Pool DHCP Primario servido por **`R1`** (HSRP Activo).
> * **`172.20.10.150 - 172.20.10.199`:** Pool DHCP Secundario servido por **`R2-Secundario`** (HSRP Standby).

---

## 2. Propuesta del Cuadro de IP Completo (Punto 2 — Figura 1 Corregida: Chiriquí y Sucursal Veraguas)

Escenario local controlado **sin acceso a Internet** (conforme a la **III Parte**), interconectando la **Sede Matriz Chiriquí (`172.20.10.0/24`)** con la nueva **Sucursal Provincia de Veraguas — Plaza Banconal, Vía Panamericana (`172.20.20.0/24`)**.

| Sede / Zona | Equipo en Packet Tracer (`Figura 1`) | Interfaz | Modo | Dirección IP | Máscara (`MR`) | Puerta de Enlace (`PE`) | `DNS1` / `DNS2` | Rol en el Sistema Chinos Café S.A. |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **Núcleo HSRP** | **VIP Chiriquí (Grupo 10)** | Virtual L3 | HSRP v2 | **`172.20.10.1`** | `255.255.255.0` | N/A | N/A | Puerta de enlace flotante Sede Chiriquí |
| **Núcleo HSRP** | **VIP Veraguas (Grupo 20)** | Virtual L3 | HSRP v2 | **`172.20.20.1`** | `255.255.255.0` | N/A | N/A | Puerta de enlace flotante Sucursal Veraguas |
| **Núcleo Central** | **`R1`** (`Cisco 2911`) | `Gig0/0` (CH)<br>`Gig0/1` (VE) | Fijo | `172.20.10.2`<br>`172.20.20.2` | `255.255.255.0`<br>`255.255.255.0` | N/A | `8.8.8.8` | **Router Primario (HSRP Active, Prio 110 + Preempt)** y DHCP `.110–.149` |
| **Núcleo Central** | **`R2-Secundario`** (`Cisco 2911`) | `Gig0/0` (CH)<br>`Gig0/1` (VE) | Fijo | `172.20.10.3`<br>`172.20.20.3` | `255.255.255.0`<br>`255.255.255.0` | N/A | `8.8.8.8` | **Router de Respaldo (HSRP Standby, Prio 100)** corregido y DHCP `.150–.199` |
| **Matriz Chiriquí** | **`SW0`** (`2960-24TT`) | `VLAN 1` + `Po1` | Fijo | `172.20.10.11` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Switch Principal Chiriquí (**STP Root Primary** + LACP `Fa0/23-24`) |
| **Matriz Chiriquí** | **`SW0-BKP`** (`2960-24TT`) | `VLAN 1` + `Po1` | Fijo | `172.20.10.12` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Switch Redundante Chiriquí (**STP Root Secondary** + LACP `Fa0/23-24`) |
| **Matriz Chiriquí** | **`SO1 LINUX BD1 / INTERFAZ WEB`** | `FastEthernet0` | **Fijo** | **`172.20.10.100`** | `255.255.255.0` | `172.20.10.1` | `172.20.10.1`<br>`8.8.8.8` | **Servidor Principal Linux:** NGINX HTTP/HTTPS (**Sitio Original Prototipo**), BD1 Principal, SSH/FTP Knockd |
| **Matriz Chiriquí** | **`LCH01`** (Laptop A) | `FastEthernet0` | Fijo | `172.20.10.101` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Estación de Desarrollo / Administración Chiriquí |
| **Matriz Chiriquí** | **`LCH02-LAPTOP-B`** (Laptop B) | `FastEthernet0` | Fijo | `172.20.10.102` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Estación de Red, Monitoreo de Réplica y Gestión |
| **Matriz Chiriquí** | **`VM-KALI-LINUX`** (Parte III) | `FastEthernet0` | Fijo | **`172.20.10.105`** | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Máquina Virtual Auditoría Seguridad (Nmap, Wireshark, Hydra, ZAP) |
| **WLAN Chiriquí** | **`AP-CH1`** y **`AP-CH2-BKP`** | `Port 0` / WLAN | Puente L2 | Capa 2 | N/A | N/A | N/A | Doble AP en Roaming — **SSID: `EXAMEN PARCIAL2`** (Canales `1` y `6`, WPA2-PSK `1234567890`) |
| **WLAN Chiriquí** | **`Tablet-CH`** | `Wireless0` | DHCP | `172.20.10.110+` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Tablet inalámbrica de pedidos en Salón Chiriquí |
| **WLAN Chiriquí** | **`Printer1`** | `Wireless0` | DHCP | `172.20.10.111+` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Impresora inalámbrica de comandas/facturas Chiriquí |
| **WLAN Chiriquí** | **`Smartphone-Yappy`** | `Wireless0` | DHCP | `172.20.10.112+` | `255.255.255.0` | `172.20.10.1` | `172.20.10.1` | Cliente móvil para pagos **YAPPY Comercial** |
| **Suc. Veraguas** | **`SW1`** (`2960-24TT`) | `VLAN 1` | Fijo | `172.20.20.11` | `255.255.255.0` | `172.20.20.1` | `172.20.10.100` | Switch Sucursal Plaza Banconal (doble uplink a `R1` y `R2-Secundario`) |
| **Suc. Veraguas** | **`SO2 LINUX BD2 / INTERFAZ WEB`** | `FastEthernet0` | **Fijo** | **`172.20.20.100`** | `255.255.255.0` | `172.20.20.1` | `172.20.10.100` | **Servidor Réplica Linux:** **BD2 Relacional Réplica** + Interfaz Web Espejo NGINX |
| **Suc. Veraguas** | **`LVE02`** | `FastEthernet0` | Fijo | `172.20.20.101` | `255.255.255.0` | `172.20.20.1` | `172.20.10.100` | Laptop operativa Sucursal Veraguas (Plaza Banconal) |
| **WLAN Veraguas** | **`AP-VERAGUAS`** | `Port 0` / WLAN | Puente L2 | Capa 2 | N/A | N/A | N/A | Access Point Sucursal — **SSID: `CHINOS VERAGUAS`** (Canal `11`, WPA2-PSK `1234567890`) |
| **WLAN Veraguas** | **`Tablet-VE`** y **`Printer0`** | `Wireless0` | DHCP | `172.20.20.110+` | `255.255.255.0` | `172.20.20.1` | `172.20.10.100` | Equipos inalámbricos corregidos de la Sucursal Veraguas |

---

## 3. Resumen de Correcciones Realizadas al Diagrama Original (`Figura 1` — Punto 3)

En la `Figura 1` del enunciado del examen existían desconexiones intencionales que fueron corregidas e integradas con alta disponibilidad:

1. **Corrección de `R2-Secundario` (antes aislado solo con cable de consola):** Se cablearon sus interfaces `GigabitEthernet0/0` y `GigabitEthernet0/1` hacia ambas sedes y se configuró **HSRP v2** junto a `R1`, logrando conmutación automática sin caída ante fallos del router primario (`VIP 172.20.10.1` en Chiriquí y `VIP 172.20.20.1` en Veraguas).
2. **Corrección de Equipos Inalámbricos Desconectados (`Tablet-CH`, `Printer1`, `Tablet-VE`, `Printer0`):** En la `Figura 1` carecían de puntos de acceso inalámbricos y tarjetas Wi-Fi en las impresoras. Se instalaron módulos inalámbricos `WMP300N` en `Printer1` y `Printer0` y se desplegaron **Access Points redundantes** (`AP-CH1` y `AP-CH2-BKP` con SSID **`EXAMEN PARCIAL2`** en Chiriquí; `AP-VERAGUAS` en Veraguas).
3. **Eliminación del Punto Único de Fallo en Conmutación LAN Chiriquí:** Se añadió `SW0-BKP` unido a `SW0` mediante **EtherChannel LACP (`Port-channel 1` en `Fa0/23` y `Fa0/24`)** y `Rapid-PVST+`.
4. **Sitio Original Prototipo Habilitado en el Servidor Simulado (Punto 4):** En `SO1 LINUX BD1 / INTERFAZ WEB` (`172.20.10.100`) y su espejo `SO2 LINUX BD2 / INTERFAZ WEB` (`172.20.20.100`) se cargaron las 4 secciones funcionales del prototipo (**Inicio, Fábrica con 6 combos + Listbox de ingredientes, Pedidos con flete/replicación y Pagos Yappy Comercial**) accesibles desde el navegador web de cualquier equipo en Packet Tracer.
