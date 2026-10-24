# Guía de Sustentación y Configuración: Topología Packet Tracer 9.0.1 (Figura 1 Corregida)

> [!IMPORTANT]
> **¡Topología 100% alineada al PDF oficial ya generada!** Los archivos `red-lan/Parcial2.pkt` y `red-lan/topologia_red_parcial2.pkt` ya contienen el esquema completo de **CHINOS CAFÉ S.A.** (Sede Matriz Chiriquí + Sucursal Provincia de Veraguas en Plaza Banconal - Vía Panamericana), corrigiendo todas las desconexiones de la **Figura 1**, aplicando los parámetros exactos de la **II Parte** (`SSID: EXAMEN PARCIAL2` con espacio, `172.20.10.100 - 199`, `PE: 172.20.10.1`, `DNS1: 172.20.10.1`, `DNS2: 8.8.8.8`), aislando la red sin Internet (**III Parte**) e integrando el **Sitio Original Prototipo completo** dentro de `SO1 LINUX BD1 / INTERFAZ WEB` (`172.20.10.100`) y su réplica `SO2 LINUX BD2 / INTERFAZ WEB` (`172.20.20.100`).

---

## 1. ¿Qué se corrigió respecto a la Figura 1 del PDF? (Para explicar en la Sustentación)

1. **`R2-Secundario` Conectado y Configurado en HSRP v2 (Capa 3):**
   * En la *Figura 1* del examen, `R2-Secundario` aparecía desconectado de los switches (solo tenía un cable de consola desde `LCH01`).
   * **Corrección:** Se cableó `R2-Secundario` hacia Chiriquí (`Gig0/0` ➔ `SW0-BKP`) y hacia Veraguas (`Gig0/1` ➔ `SW1`), configurando **HSRP v2** junto a `R1`:
     * **Chiriquí (Grupo 10):** Gateway Virtual Flotante **`172.20.10.1`** (`R1` `.2` *Active* Prio `110 + preempt`; `R2-Secundario` `.3` *Standby* Prio `100`).
     * **Veraguas (Grupo 20):** Gateway Virtual Flotante **`172.20.20.1`** (`R1` `.2` *Active* Prio `110 + preempt`; `R2-Secundario` `.3` *Standby* Prio `100`).
2. **Cobertura Inalámbrica Real para Equipos Flotantes (`Tablet-CH`, `Printer1`, `Tablet-VE`, `Printer0`):**
   * En la *Figura 1*, las impresoras y tablets no tenían Access Points ni tarjetas Wi-Fi.
   * **Corrección:** Se instalaron tarjetas inalámbricas `Linksys-WMP300N` en `Printer1` y `Printer0`, y se desplegaron **Access Points redundantes**:
     * **Chiriquí:** `AP-CH1` (Canal 1) + `AP-CH2-BKP` (Canal 6) con **SSID `EXAMEN PARCIAL2`** *(con espacio)* y WPA2-PSK (AES) `1234567890`.
     * **Veraguas:** `AP-VERAGUAS` (Canal 11) con **SSID `CHINOS VERAGUAS`** y WPA2-PSK (AES) `1234567890`.
3. **Redundancia de Conmutación LAN (Capa 2 — EtherChannel LACP + Rapid-PVST+):**
   * Se agregó `SW0-BKP` en Chiriquí unido a `SW0` mediante **`Port-channel 1` (`Fa0/23` y `Fa0/24`)**, evitando que la caída de un switch deje fuera al servidor o a los equipos de auditoría.
4. **DHCP Redundante (*Split-Scope*) con Parámetros Oficiales:**
   * Rango oficial `172.20.10.100 - 199` (`MR: 255.255.255.0`, `PE: 172.20.10.1`, `DNS1: 172.20.10.1`, `DNS2: 8.8.8.8`), reservando `.100–.109` para el servidor fijo (`172.20.10.100`) y laptops/VMs, repartiendo `.110–.149` desde `R1` y `.150–.199` desde `R2-Secundario`.
5. **Sección WEB — Sitio Original Prototipo en el Servidor Simulado (Punto 4):**
   * Tanto `SO1 LINUX BD1 / INTERFAZ WEB` (`172.20.10.100`) como `SO2 LINUX BD2 / INTERFAZ WEB` (`172.20.20.100`) tienen activos **HTTP y HTTPS** con las **4 páginas navegables del prototipo de Chinos Café S.A.**:
     * `index.html` — Portada corporativa y menú de **6 Combos de Pizza** (superando el mínimo de 5 exigido).
     * `fabrica.html` — CRUD de Pizzas con **Listbox de ingredientes (mín. 2, máx. 10)**, Combo Box de refrescos e ítem adicional.
     * `pedidos.html` — Selección de combo en Combo Box, cálculo de flete/retiro, envío JSON por correo y replicación `BD1 ⟷ BD2`.
     * `pagos.html` — Confirmación de pago por **YAPPY Comercial** y despacho al cliente.

---

## 2. Las 5 Demostraciones en Vivo frente al Profesor (Guion de Sustentación)

> **Al abrir `red-lan/Parcial2.pkt`:** Presiona una vez el botón **Fast Forward Time (`Alt + D`)** abajo a la izquierda para adelantar 30 segundos simulados y que todas las tablets/impresoras reciban su IP por DHCP de inmediato. *(Opcional: para mostrar las ondas punteadas de Wi-Fi, ve a `Options ➔ Preferences ➔ Hide` y desmarca `Hide Wireless/Cellular Connection`).*

### Demo 1: Navegar el Sitio Original Prototipo dentro de Packet Tracer (Punto 4)
1. Haz clic en **`LCH01`** (o en **`Tablet-CH`** / **`LVE02`**) ➔ pestaña **Desktop** ➔ **Web Browser**.
2. Escribe `http://172.20.10.100` (o `https://172.20.10.100`) y pulsa **Go**.
3. Navega en vivo frente al profesor por **Inicio ➔ Fábrica (CRUD Pizzas) ➔ Pedidos ➔ Pagos (YAPPY)** e incluso pulsa los botones de guardar/confirmar.
4. Luego escribe `http://172.20.20.100` para demostrar cómo responde el servidor espejo y réplica **`SO2 LINUX BD2 / INTERFAZ WEB`** en la Sucursal de Veraguas (Plaza Banconal).

### Demo 2: Validar DHCP Inalámbrico en `EXAMEN PARCIAL2` (Punto 1)
1. Haz clic en **`Tablet-CH`**, **`Printer1`** o **`Smartphone-Yappy`** ➔ **Desktop ➔ IP Configuration**.
2. Muestra cómo obtuvieron automáticamente una IP dentro de **`172.20.10.110 - 199`**, máscara **`255.255.255.0`**, Gateway **`172.20.10.1`** y DNS **`172.20.10.1`**.

### Demo 3: Tolerancia a Fallos de Router HSRP (`R1` ➔ `R2-Secundario`)
1. Abre **`VM-KALI-LINUX`** (`172.20.10.105`) ➔ **Command Prompt** y ejecuta `ping 172.20.20.100` (llega hasta el servidor `SO2` en Veraguas).
2. Abre **`R1`** ➔ pestaña **Physical** y apaga su interruptor de corriente.
3. Pulsa **Fast Forward Time (`Alt + D`)** una vez y vuelve a hacer `ping 172.20.20.100` o abre `http://172.20.20.100` desde `LCH01`: **¡la red entre Chiriquí y Veraguas sigue operando sin interrupción a través de `R2-Secundario` (`show standby brief`)!**

### Demo 4: Tolerancia a Fallos en Capa 2 (`EtherChannel LACP Po1`)
1. Con la herramienta **Delete (`X`)**, corta **uno** de los dos cables cruzados entre `SW0` y `SW0-BKP`.
2. Desde **`VM-KALI-LINUX`** (`172.20.10.105`, en `SW0-BKP`) haz `ping 172.20.10.100` hacia `SO1` (en `SW0`): **0% pérdida de paquetes**, el segundo enlace del `Port-channel 1` mantiene la troncal activa.

### Demo 5: Tolerancia a Fallos Inalámbrica (Doble AP en Chiriquí)
1. Elimina el cable o apaga **`AP-CH1`**: `Tablet-CH`, `Printer1` y `Smartphone-Yappy` migran automáticamente en *roaming* hacia **`AP-CH2-BKP`** conservando el SSID **`EXAMEN PARCIAL2`**.
