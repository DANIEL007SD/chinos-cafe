# Fix HSRP — Failover no funcionaba durante prueba de corte de R1

**Fecha:** 2026-11-10 12:30
**Síntoma:** Al desconectar el cable R1↔switch, los pings SO1↔SO2 no recibían respuesta durante el corte.

## Diagnóstico (con `show standby brief`)

**R1 (Active, antes del fix):**
```
Interface  Grp  Pri  P State    Active  Standby      Virtual IP
Gig0/0     10   110  P Active   local   172.20.10.3  172.20.10.1
Gig0/1     20   110  P Active   local   172.20.20.3  172.20.20.1
```

**R2-Secundario (Standby, antes del fix):**
```
Interface  Grp  Pri  P State    Active        Standby  Virtual IP
Gig0/0     10   100    Standby  172.20.10.2   local    172.20.10.1
Gig0/1     20   100    Standby  172.20.20.2   local    172.20.20.1
                  ^
                  SIN "P" (preempt)
```

## Dos problemas detectados
1. **R2 sin preempt.** Cuando R1 se recupera, R2 no cedía Active → el failback nunca ocurría correctamente.
2. **Timers HSRP por defecto (hello 3s / hold 10s).** Durante los ~10 segundos posteriores al corte de R1, nadie respondía al VIP → **los pings fallaban en ese agujero**. Ese fue el síntoma real que observaste.

## Correcciones aplicadas (ambos routers)

**En R2-Secundario:**
```
conf t
 interface g0/0
  standby 10 preempt
  standby 10 timers 1 3
 interface g0/1
  standby 20 preempt
  standby 20 timers 1 3
end
write memory
```

**En R1 (solo timers; ya tenía preempt):**
```
conf t
 interface g0/0
  standby 10 timers 1 3
 interface g0/1
  standby 20 timers 1 3
end
write memory
```

## Resultado esperado
- Failover HSRP ahora en **~3 segundos** (antes ~10s).
- R2 toma los VIPs al caer R1 y los **devuelve** cuando R1 vuelve (preempt).
- Pings SO1↔SO2 deben seguir fluyendo con como máximo 2–3 paquetes perdidos durante la transición.

## Volver a probar
1. En SO1 Server (`172.20.10.100`), abrir Command Prompt.
2. `ping 172.20.20.100 -n 30` (30 paquetes).
3. Mientras corre, desconectar el enlace R1 ↔ SW0-BKP.
4. Esperar ~5 s, reconectar.
5. Revisar las estadísticas: deben ser ≥ 85 % de respuestas exitosas.

## Captura
- `20261110_1231_pt_hsrp_fix_aplicado.jpg` — topología después del fix y guardado del `.pkt`.

> La captura con la prueba real del failover (Inicio/Proceso/Resultado) se tomará cuando el usuario vuelva a correr la secuencia arriba.
