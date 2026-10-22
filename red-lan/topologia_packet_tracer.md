# Guía de Construcción: Topología de Red en Cisco Packet Tracer

Esta guía detalla los pasos para recrear la topología de red del Parcial 2 en **Cisco Packet Tracer** y exportar el archivo `.pkt` junto a las capturas correspondientes.

---

## 1. Dispositivos Necesarios en Packet Tracer

| Dispositivo | Modelo en Packet Tracer | Nombre Lógico | Conexión |
| :--- | :--- | :--- | :--- |
| **Router Inalámbrico** | `WRT300N` o `Home Router` | `Router_WiFi_EXAMEN` | Central |
| **Switch de Distribución** | `Cisco Catalyst 2960-24TT` | `SW-CORE-01` | Cable directo (`Copper Straight-Through`) |
| **Laptop A** | `Laptop-PT` | `Laptop-A-Desarrollo` | Módulo Wi-Fi `WPC300N` |
| **Servidor VM Laptop A** | `Server-PT` | `Servidor-Web-Flask-NGINX` | Cable directo a Switch / Wi-Fi |
| **Laptop B** | `Laptop-PT` | `Laptop-B-Red-Replica` | Módulo Wi-Fi `WPC300N` |
| **VM Kali Linux (Atacante)**| `PC-PT` | `Kali-Linux-Atacante` | Cable directo / Wi-Fi |
| **Servidor BD Réplica** | `Server-PT` | `BD-MySQL-Replica` | Cable directo al Switch |

---

## 2. Configuración Paso a Paso en Packet Tracer

### Paso 1: Configurar el Router Inalámbrico (`Router_WiFi_EXAMEN`)
1. Abrir la pestaña **Config** > **LAN**:
   - **IP Address:** `172.20.10.1`
   - **Subnet Mask:** `255.255.255.0`
2. Pestaña **GUI** (o **Wireless**):
   - **Network Name (SSID):** `EXAMEN PARCIAL2`
   - **Wireless Security:** `WPA2 Personal`
   - **Encryption:** `AES`
   - **Pre-Shared Key (Passphrase):** `Parcial2026*` (o la contraseña acordada)
3. Pestaña **GUI** > **Setup** > **Basic Setup** (DHCP):
   - **DHCP Server:** `Enabled`
   - **Start IP Address:** `172.20.10.100`
   - **Maximum number of Users:** `50`
   - **DNS 1:** `172.20.10.1`
   - Clic en **Save Settings**.

---

### Paso 2: Configurar las Laptops con Wi-Fi
Para `Laptop-A-Desarrollo` y `Laptop-B-Red-Replica`:
1. Hacer clic en la Laptop > pestaña **Physical**.
2. **Apagar** la laptop con el botón de encendido.
3. Arrastrar el puerto Ethernet `PT-LAPTOP-NM-1CFE` a la lista de módulos para quitarlo.
4. Arrastrar el módulo inalámbrico **`WPC300N`** a la bahía vacía.
5. **Encender** la laptop de nuevo.
6. Ir a la pestaña **Desktop** > **PC Wireless** > pestaña **Connect**:
   - Dar clic en **Refresh**.
   - Seleccionar `EXAMEN PARCIAL2` y dar clic en **Connect**.
   - Introducir la clave WPA2 y verificar que aparezca la señal de conexión.
7. En **Desktop** > **IP Configuration**, verificar que reciba IP vía DHCP en el rango `172.20.10.10X`.

---

### Paso 3: Configurar el Servidor Web (Laptop A)
1. Clic en `Servidor-Web-Flask-NGINX` > **Desktop** > **IP Configuration**:
   - **IP Configuration:** Estática
   - **IP Address:** `172.20.10.102`
   - **Subnet Mask:** `255.255.255.0`
   - **Default Gateway:** `172.20.10.1`
   - **DNS Server:** `172.20.10.1`
2. Ir a la pestaña **Services** > **HTTP**:
   - Asegurar que **HTTP** y **HTTPS** estén en **ON**.
   - Editar `index.html` para simular la app:
     ```html
     <html>
       <h1>Chinos Cafe - App Web Flask NGINX</h1>
       <p>Servidor Principal - 172.20.10.102</p>
     </html>
     ```

---

### Paso 4: Configurar la BD Réplica y la VM Kali (Laptop B)
1. `BD-MySQL-Replica`:
   - Asignar IP estática: `172.20.10.104` (o `172.20.10.103` asociada a Laptop B)
   - Máscara: `255.255.255.0` | Gateway: `172.20.10.1`
2. `Kali-Linux-Atacante`:
   - Asignar IP: `172.20.10.105`
   - Máscara: `255.255.255.0` | Gateway: `172.20.10.1`

---

## 3. Pruebas de Validación dentro de Packet Tracer

1. **Prueba de Conectividad (Ping):**
   - Desde `Kali-Linux-Atacante` (Command Prompt):
     ```
     ping 172.20.10.102
     ```
     *Debe responder 4/4 exitosos.*
2. **Prueba de Servicio Web:**
   - Desde `Kali-Linux-Atacante` > **Desktop** > **Web Browser**:
     - Escribir `http://172.20.10.102` y dar Go.
     - Debe cargar la página de bienvenida de Chinos Café.
3. **Modo Simulación:**
   - Cambiar a modo **Simulation** en Packet Tracer.
   - Filtrar eventos por `ICMP`, `HTTP`, `TCP`, `DNS`.
   - Enviar un paquete PDU desde Kali hacia el Servidor Web para capturar visualmente el flujo de paquetes y tomar captura de pantalla para el informe.

---

## 4. Guardado y Entrega
* Guardar el archivo en esta carpeta con el nombre:
  `red-lan/topologia_red_parcial2.pkt`
* Guardar las capturas de pantalla de la topología y de los pings exitosos en:
  `red-lan/evidencias/`
