# Guía Paso a Paso: Red Empresarial Redundante en Cisco Packet Tracer 9.0.1

Esta guía te lleva desde un archivo en blanco hasta una **topología completa con redundancia multicapa** lista para sustentar en el **Examen Parcial 2**.

## Resumen de Redundancias Implementadas (Para explicar al Profesor)

1. **Redundancia de Capa 3 (HSRP — Hot Standby Router Protocol):** Dos routers Cisco 2911 (`R1-PRINCIPAL` y `R2-RESPALDO`) comparten la puerta de enlace virtual **`172.20.10.1`**. Si `R1` falla o se apaga en plena demostración, `R2` asume el tráfico automáticamente sin desconectar la red.
2. **Redundancia DHCP (Split-Scope):** `R1` reparte `172.20.10.110–149` y `R2` reparte `172.20.10.150–199` (ambos dentro del rango `172.20.10.100–199`), garantizando asignación de IP aunque caiga un router.
3. **Redundancia de Capa 2 (EtherChannel LACP + Rapid-PVST+):** Dos switches Catalyst 2960 unidos por un enlace doble agregado (`Port-channel 1` en `Fa0/23` y `Fa0/24`). Si se corta un cable físico entre los switches, el otro mantiene la comunicación sin perder paquetes.
4. **Redundancia Inalámbrica (Doble Access Point en Roaming):** Dos puntos de acceso (`AP1` en canal 1 y `AP2` en canal 6) emitiendo el SSID **`EXAMENPARCIAL2`** con WPA2-PSK **`1234567890`**.
5. **Redundancia de Datos (BD Local + Réplica Cloud Supabase):** Servidor principal `SRV-CHINOS-WEB` (`172.20.10.100`) en la LAN y servidor `SRV-SUPABASE-REPLICA` (`203.0.113.10`) en el segmento WAN/Cloud accesible por ambos routers mediante NAT redundante.

---

## PASO 1: Colocar los Dispositivos en el Lienzo

Abre **Cisco Packet Tracer** y arrastra los siguientes equipos desde el menú inferior izquierdo:

| Categoría en Packet Tracer | Subcategoría | Modelo Exacto | Cantidad | Nombres a ponerles (doble clic en la etiqueta) |
| :--- | :--- | :--- | :---: | :--- |
| **Network Devices** | **Routers** | `2911` | **2** | `R1-PRINCIPAL` y `R2-RESPALDO` |
| **Network Devices** | **Switches** | `2960` (`2960-24TT`) | **3** | `SW1-CORE`, `SW2-REDUNDANTE` y `SW-WAN-ISP` |
| **Network Devices** | **Wireless Devices** | `AP-PT` | **2** | `AP1-WIFI-CH1` y `AP2-WIFI-CH6` |
| **End Devices** | **End Devices** | `Server` (`Server-PT`) | **2** | `SRV-CHINOS-WEB` y `SRV-SUPABASE-REPLICA` |
| **End Devices** | **End Devices** | `PC` (`PC-PT`) | **1** | `VM-KALI-LINUX` |
| **End Devices** | **End Devices** | `Laptop` (`Laptop-PT`) | **3** | `LAPTOP-A-DEV`, `LAPTOP-B-ADMIN` y `CLIENTE-WIFI` |
| **End Devices** | **End Devices** | `Smartphone` (`SmartPhone-PT`) | **1** | `CELULAR-YAPPY` |

> **Tip visual:** Ubica `SRV-SUPABASE-REPLICA` y `SW-WAN-ISP` arriba del todo (Zona Cloud/WAN), debajo coloca `R1-PRINCIPAL` (izquierda) y `R2-RESPALDO` (derecha), debajo `SW1-CORE` y `SW2-REDUNDANTE`, y abajo los servidores, laptops, Kali y Access Points.

---

## PASO 2: Cableado Exacto Puerto por Puerto

En el ícono del **Rayo naranja (Connections)**:

### A. Cables Directos (`Copper Straight-Through` — línea negra continua)
Conecta exactamente estos puertos:

1. **Zona WAN (Nube / Supabase):**
   * `SRV-SUPABASE-REPLICA` (`FastEthernet0`) ➔ `SW-WAN-ISP` (`FastEthernet0/1`)
   * `R1-PRINCIPAL` (`GigabitEthernet0/1`) ➔ `SW-WAN-ISP` (`FastEthernet0/2`)
   * `R2-RESPALDO` (`GigabitEthernet0/1`) ➔ `SW-WAN-ISP` (`FastEthernet0/3`)

2. **Routers hacia Switches LAN:**
   * `R1-PRINCIPAL` (`GigabitEthernet0/0`) ➔ `SW1-CORE` (`GigabitEthernet0/1`)
   * `R2-RESPALDO` (`GigabitEthernet0/0`) ➔ `SW2-REDUNDANTE` (`GigabitEthernet0/1`)

3. **Equipos por Ethernet en `SW1-CORE` (Lado Laptop A / Servidor):**
   * `SW1-CORE` (`FastEthernet0/1`) ➔ `SRV-CHINOS-WEB` (`FastEthernet0`)
   * `SW1-CORE` (`FastEthernet0/2`) ➔ `LAPTOP-A-DEV` (`FastEthernet0`)
   * `SW1-CORE` (`FastEthernet0/10`) ➔ `AP1-WIFI-CH1` (`Port 0`)

4. **Equipos por Ethernet en `SW2-REDUNDANTE` (Lado Laptop B / Kali):**
   * `SW2-REDUNDANTE` (`FastEthernet0/1`) ➔ `VM-KALI-LINUX` (`FastEthernet0`)
   * `SW2-REDUNDANTE` (`FastEthernet0/2`) ➔ `LAPTOP-B-ADMIN` (`FastEthernet0`)
   * `SW2-REDUNDANTE` (`FastEthernet0/10`) ➔ `AP2-WIFI-CH6` (`Port 0`)

### B. Cables Cruzados (`Copper Cross-Over` — línea negra punteada) para EtherChannel
Une ambos switches LAN con **dos cables cruzados** para formar el canal redundante:
* `SW1-CORE` (`FastEthernet0/23`) ➔ `SW2-REDUNDANTE` (`FastEthernet0/23`)
* `SW1-CORE` (`FastEthernet0/24`) ➔ `SW2-REDUNDANTE` (`FastEthernet0/24`)

---

## PASO 3: Configuración CLI de Switches y Routers (Copiar y Pegar)

### 1. Configurar `SW1-CORE`
Haz clic en `SW1-CORE` ➔ pestaña **CLI**, presiona `Enter` y pega este bloque:

```ios
enable
configure terminal
hostname SW1-CORE
no ip domain-lookup
spanning-tree mode rapid-pvst
spanning-tree vlan 1 root primary

interface range fa0/23 - 24
 switchport mode trunk
 channel-group 1 mode active
 no shutdown
exit

interface port-channel 1
 switchport mode trunk
exit

interface range fa0/1 - 10
 switchport mode access
 spanning-tree portfast
exit

interface vlan 1
 ip address 172.20.10.11 255.255.255.0
 no shutdown
exit

ip default-gateway 172.20.10.1
end
write memory
```

---

### 2. Configurar `SW2-REDUNDANTE`
Haz clic en `SW2-REDUNDANTE` ➔ pestaña **CLI**, presiona `Enter` y pega este bloque:

```ios
enable
configure terminal
hostname SW2-REDUNDANTE
no ip domain-lookup
spanning-tree mode rapid-pvst
spanning-tree vlan 1 root secondary

interface range fa0/23 - 24
 switchport mode trunk
 channel-group 1 mode active
 no shutdown
exit

interface port-channel 1
 switchport mode trunk
exit

interface range fa0/1 - 10
 switchport mode access
 spanning-tree portfast
exit

interface vlan 1
 ip address 172.20.10.12 255.255.255.0
 no shutdown
exit

ip default-gateway 172.20.10.1
end
write memory
```

---

### 3. Configurar `R1-PRINCIPAL` (HSRP Activo + DHCP Primario + NAT)
Haz clic en `R1-PRINCIPAL` ➔ pestaña **CLI** (si pregunta `Would you like to enter the initial configuration dialog? [yes/no]:` escribe **`no`** y presiona `Enter`). Luego pega:

```ios
enable
configure terminal
hostname R1-PRINCIPAL
no ip domain-lookup

ip dhcp excluded-address 172.20.10.1 172.20.10.109
ip dhcp excluded-address 172.20.10.150 172.20.10.254

ip dhcp pool LAN_EXAMEN_PRIMARIO
 network 172.20.10.0 255.255.255.0
 default-router 172.20.10.1
 dns-server 172.20.10.100
exit

interface GigabitEthernet0/0
 description LAN_GATEWAY_ACTIVO
 ip address 172.20.10.2 255.255.255.0
 ip nat inside
 standby version 2
 standby 10 ip 172.20.10.1
 standby 10 priority 110
 standby 10 preempt
 no shutdown
exit

interface GigabitEthernet0/1
 description WAN_SUPABASE
 ip address 203.0.113.2 255.255.255.0
 ip nat outside
 standby version 2
 standby 20 ip 203.0.113.1
 standby 20 priority 110
 standby 20 preempt
 no shutdown
exit

access-list 1 permit 172.20.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

end
write memory
```

---

### 4. Configurar `R2-RESPALDO` (HSRP Standby + DHCP Respaldo + NAT)
Haz clic en `R2-RESPALDO` ➔ pestaña **CLI** (escribe **`no`** si pregunta por el asistente inicial) y pega:

```ios
enable
configure terminal
hostname R2-RESPALDO
no ip domain-lookup

ip dhcp excluded-address 172.20.10.1 172.20.10.149
ip dhcp excluded-address 172.20.10.200 172.20.10.254

ip dhcp pool LAN_EXAMEN_RESPALDO
 network 172.20.10.0 255.255.255.0
 default-router 172.20.10.1
 dns-server 172.20.10.100
exit

interface GigabitEthernet0/0
 description LAN_GATEWAY_STANDBY
 ip address 172.20.10.3 255.255.255.0
 ip nat inside
 standby version 2
 standby 10 ip 172.20.10.1
 standby 10 priority 100
 no shutdown
exit

interface GigabitEthernet0/1
 description WAN_SUPABASE_BACKUP
 ip address 203.0.113.3 255.255.255.0
 ip nat outside
 standby version 2
 standby 20 ip 203.0.113.1
 standby 20 priority 100
 no shutdown
exit

access-list 1 permit 172.20.10.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet0/1 overload

end
write memory
```

---

## PASO 4: Configurar los 2 Access Points (`EXAMENPARCIAL2`)

1. Haz clic en **`AP1-WIFI-CH1`** ➔ pestaña **Config** ➔ **Port 1**:
   * **SSID:** `EXAMENPARCIAL2`
   * **Channel:** `1`
   * **Authentication:** Marca **`WPA2-PSK`**
   * **PSK Pass Phrase:** `1234567890`
   * **Encryption Type:** `AES`
2. Haz clic en **`AP2-WIFI-CH6`** ➔ pestaña **Config** ➔ **Port 1**:
   * **SSID:** `EXAMENPARCIAL2`
   * **Channel:** `6` *(canal distinto para evitar solapamiento y permitir roaming)*
   * **Authentication:** Marca **`WPA2-PSK`**
   * **PSK Pass Phrase:** `1234567890`
   * **Encryption Type:** `AES`

---

## PASO 5: Configurar Servidores, Laptops, Kali y Clientes Wi-Fi

### 1. Servidor Principal `SRV-CHINOS-WEB` (`172.20.10.100`)
* **Desktop ➔ IP Configuration (Static):**
  * **IPv4 Address:** `172.20.10.100`
  * **Subnet Mask:** `255.255.255.0`
  * **Default Gateway:** `172.20.10.1`
  * **DNS Server:** `172.20.10.100`
* **Services ➔ HTTP:**
  * Verifica que **HTTP** y **HTTPS** estén en **On**.
  * Haz clic en *edit* sobre `index.html`, reemplázalo por esto y pulsa **Save**:
    ```html
    <html>
    <body style="font-family:Arial;background:#fff8f0;padding:20px;">
      <h1 style="color:#b91c1c;">CHINOS CAFE S.A. - Servidor NGINX + Flask</h1>
      <hr>
      <p><b>Nodo Primario LAN:</b> 172.20.10.100 (HTTP/HTTPS Activo)</p>
      <p><b>Gateway Redundante HSRP:</b> 172.20.10.1</p>
      <p><b>Estado Replica Supabase:</b> Sincronizado en tiempo real</p>
    </body>
    </html>
    ```
* **Services ➔ DNS:**
  * Cambia **DNS Service** a **`On`**.
  * Agrega dos registros tipo `A Record` (clic en **Add** tras cada uno):
    1. **Name:** `chinoscafe.local` | **Address:** `172.20.10.100`
    2. **Name:** `supabase.replica.cloud` | **Address:** `203.0.113.10`

### 2. Servidor Réplica Cloud `SRV-SUPABASE-REPLICA` (`203.0.113.10`)
* **Desktop ➔ IP Configuration (Static):**
  * **IPv4 Address:** `203.0.113.10`
  * **Subnet Mask:** `255.255.255.0`
  * **Default Gateway:** `203.0.113.1`
* **Services ➔ HTTP:**
  * Deja **HTTP** y **HTTPS** en **On**, edita `index.html` y guarda:
    ```html
    <html>
    <body style="font-family:Arial;background:#ecfdf5;padding:20px;">
      <h1 style="color:#047857;">SUPABASE CLOUD - PostgreSQL Replica</h1>
      <hr>
      <p><b>Proyecto:</b> talewwtbjoyfsoresvmx.supabase.co (203.0.113.10)</p>
      <p><b>Tablas activas:</b> public.pedido_replica | public.pago_replica</p>
    </body>
    </html>
    ```

### 3. Equipos Cableados por Ethernet (`Static` o `DHCP`)
En **Desktop ➔ IP Configuration** asigna:
* **`LAPTOP-A-DEV`:** IP `172.20.10.101`, Máscara `255.255.255.0`, Gateway `172.20.10.1`, DNS `172.20.10.100`.
* **`LAPTOP-B-ADMIN`:** IP `172.20.10.102`, Máscara `255.255.255.0`, Gateway `172.20.10.1`, DNS `172.20.10.100`.
* **`VM-KALI-LINUX`:** IP `172.20.10.105`, Máscara `255.255.255.0`, Gateway `172.20.10.1`, DNS `172.20.10.100`.

### 4. Clientes Inalámbricos (`CELULAR-YAPPY` y `CLIENTE-WIFI`)
* **`CELULAR-YAPPY`:**
  1. Clic en el teléfono ➔ **Config ➔ Wireless0**:
     * **SSID:** `EXAMENPARCIAL2`
     * **WPA2-PSK / Pass Phrase:** `1234567890`
  2. En **Desktop ➔ IP Configuration**, marca **DHCP** (recibirá `172.20.10.110+` automáticamente).
* **`CLIENTE-WIFI` (`Laptop-PT`):**
  1. Pestaña **Physical** ➔ apaga la laptop en su botón de encendido ➔ arrastra su tarjeta Ethernet hacia afuera y coloca el módulo **`WPC300N`** ➔ enciéndela de nuevo.
  2. Pestaña **Desktop ➔ PC Wireless ➔ Connect** ➔ **Refresh** ➔ elige `EXAMENPARCIAL2` ➔ **Connect** ➔ clave `1234567890`.
  3. Verifica en **IP Configuration** que tenga IP por **DHCP** (`172.20.10.111+`).

---

## PASO 6: Decoración Profesional para la Presentación

Usa la herramienta de rectángulos de colores (**Draw Rectangle** en la barra superior) y notas (**Place Note `N`**) para delimitar 3 zonas visuales:
* **Recuadro Azul claro (Arriba):** `ZONA CLOUD / WAN — Réplica Supabase (203.0.113.0/24)`
* **Recuadro Verde claro (Centro):** `NÚCLEO REDUNDANTE — HSRP (VIP 172.20.10.1) + EtherChannel LACP`
* **Recuadro Amarillo claro (Abajo):** `LAN LABORATORIO — 172.20.10.0/24 | SSID: EXAMENPARCIAL2`

Guarda tu proyecto en:
`red-lan/topologia_red_parcial2.pkt`

---

## PASO 7: Las 4 Demostraciones en Vivo frente al Profesor

1. **Acceso por Nombre DNS a la App y a Supabase:**
   * Abre `VM-KALI-LINUX` ➔ **Web Browser** ➔ entra a `https://chinoscafe.local` y luego a `https://supabase.replica.cloud`. ¡Ambas cargan!
2. **Prueba de Caída de Cable en EtherChannel (Capa 2):**
   * Con la herramienta **Delete (`X`)**, borra **uno** de los dos cables cruzados entre `SW1-CORE` y `SW2-REDUNDANTE`.
   * Haz `ping 172.20.10.100` desde `VM-KALI-LINUX`: **0% de pérdida**, el segundo enlace del Port-Channel mantiene todo arriba.
3. **Prueba de Caída del Router Principal HSRP (Capa 3):**
   * Abre `R1-PRINCIPAL` ➔ pestaña **Physical** y apaga su interruptor de corriente (o borra el cable `R1`–`SW1`).
   * Adelanta el reloj 10 segundos con el botón **Fast Forward Time (`Alt+D`)**.
   * Desde `VM-KALI-LINUX` ejecuta `ping 172.20.10.1` y abre `https://supabase.replica.cloud` en el navegador: **sigue funcionando gracias a `R2-RESPALDO` (`show standby brief`)**.
4. **Prueba de Caída de un Access Point Wi-Fi:**
   * Desconecta `AP1-WIFI-CH1`: el `CELULAR-YAPPY` y `CLIENTE-WIFI` se pasan automáticamente a `AP2-WIFI-CH6` manteniendo el SSID `EXAMENPARCIAL2`.
