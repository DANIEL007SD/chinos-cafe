# Cómo hacer la demo de failover HSRP en Packet Tracer

## Por qué fallaba tu prueba

Desconectaste el cable **R1 ↔ SW0** (lado Chiriquí). Eso deja a R1 así:
- `Gi0/0` (hacia Chiriquí) → **DOWN** → HSRP Grp 10 cede a R2 ✓
- `Gi0/1` (hacia Veraguas) → **UP** → HSRP Grp 20 sigue **Active en R1** ✗

Resultado: SO2 pingea a `172.20.10.100` → envía al VIP de Veraguas `172.20.20.1` que sigue en **R1** → R1 recibe pero su Gi0/0 está DOWN → responde `172.20.20.2: Destination host unreachable`.

## Por qué no se puede "arreglar" con CLI en PT

La solución canónica es **HSRP interface tracking**: cuando R1 pierde Gi0/0, HSRP también cede Grp 20 en Gi0/1. Requiere:
```
track 1 interface GigabitEthernet0/0 line-protocol
interface g0/1
 standby 20 track 1 decrement 20
```
**Packet Tracer 9.0.1 no implementa el comando `track` global** → sintaxis rechazada. Es una limitación del simulador, no del diseño HSRP.

## Cómo demostrar el failover correctamente (3 opciones)

### Opción A (RECOMENDADA): apagar R1 completo con botón de power
1. Click en R1 → pestaña **Physical**.
2. En la foto del router, click al botón redondo de power del chasis (abajo a la izquierda del rack). El router queda sin energía.
3. HSRP en R2 toma Active en ambos grupos en ~3s (con los nuevos timers).
4. SO1 ↔ SO2 debe recuperarse después de 2–3 paquetes perdidos.
5. Enciende R1 de nuevo → R2 devuelve Active a R1 por preempt.

### Opción B: desconectar AMBOS cables de R1
Quita el enlace R1↔SW0-BKP **y** R1↔SW1 al mismo tiempo. Mismo efecto que apagar power.

### Opción C: shutdown administrativo de ambas interfaces (vía CLI)
```
en
conf t
int g0/0
 shutdown
int g0/1
 shutdown
end
```
Luego para recuperar: `no shutdown` en ambas.

## Qué demostrar de la CAPA 2 (EtherChannel/STP) en su lugar

Si lo que quieres mostrar es la redundancia **del lado Chiriquí** (no HSRP), usa el failover de **SW0 ↔ SW0-BKP** o del **EtherChannel Po1**:
- Desconectar uno de los dos enlaces del Port-channel 1 — el otro sigue pasando tráfico (LACP).
- Desconectar un switch completo (SW0 o SW0-BKP) — el otro mantiene la LAN con el gateway VIP.

Esas demos sí funcionan sin requerir `track`.

## Resumen para el informe
> *"HSRP en R1 y R2 está configurado con prioridad 110/100, preempt y timers hello=1/hold=3. El failover se demuestra cortando la energía de R1 (Physical → Power), no desconectando un cable individual, ya que Packet Tracer 9.0.1 no soporta `track interface` para forzar la cesión simétrica de ambos grupos HSRP ante corte parcial de R1."*
