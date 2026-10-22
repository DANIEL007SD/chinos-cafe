# Guía de Implementación: Base de Datos Réplica en Supabase (Laptop B)

Esta guía detalla paso a paso cómo montar la **Base de Datos Réplica en la Nube con Supabase (PostgreSQL)** para el Parcial 2.

---

## 1. ¿Por qué Supabase es ideal para la Réplica?

1. **Dashboard en Vivo:** Permite mostrarle al profesor en tiempo real en la pantalla de Laptop B cómo los pedidos y pagos procesados en Laptop A se reflejan al instante en la nube.
2. **Motor PostgreSQL Robusto:** Cuenta con soporte nativo de JSON (`JSONB`), políticas de seguridad RLS (Row Level Security) y auditoría con timestamps automáticos.
3. **Cero conflictos de puertos locales:** Al estar en la nube, no compite con otros servicios locales y ambas laptops tienen acceso instantáneo mediante API REST o conexión directa a PostgreSQL.

---

## 2. Paso a Paso: Configurar el Proyecto en Supabase

### Paso 1: Crear la Cuenta y Proyecto
1. Ingresar a [supabase.com](https://supabase.com/) e iniciar sesión (puedes entrar con tu cuenta de GitHub).
2. Hacer clic en **New Project**.
3. Configurar los campos:
   * **Name:** `chinos-cafe-replica`
   * **Database Password:** Crea una contraseña segura (ej. `ChinosCafe2026*!`) y anótala.
   * **Region:** Seleccionar `US East (North Virginia)` o la más cercana para menor latencia.
   * **Pricing Plan:** `Free Plan` ($0).
4. Clic en **Create new project** (tarda ~1-2 minutos en aprovisionar).

---

### Paso 2: Crear las Tablas en Supabase
1. En el menú lateral izquierdo de tu proyecto Supabase, entra a **SQL Editor**.
2. Haz clic en **New query**.
3. Copia y pega el contenido completo del archivo:
   [schema_supabase.sql](file:///c:/Users/willi/OneDrive/Documentos/Trabajos%20Universidad/Ingenier%C3%ADa%20Web/Parcial%202/db-replica/schema_supabase.sql)
4. Haz clic en el botón verde **Run**.
5. Ve a **Table Editor** en el menú lateral y verifica que aparezcan las tablas:
   * `productos`
   * `pedidos`
   * `pagos`
   * `sync_logs`

---

### Paso 3: Obtener las Credenciales de Conexión
1. En el menú lateral izquierdo, ve al ícono de engranaje **Project Settings** > **API**.
2. Copia los siguientes dos valores:
   * **Project URL:** `https://xxxxxxxxxxxxxxxxxxxx.supabase.co`
   * **Project API Keys (`anon` / `public` o `service_role`):** Copia la clave secreta.
3. Abre el archivo [sync_engine.py](file:///c:/Users/willi/OneDrive/Documentos/Trabajos%20Universidad/Ingenier%C3%ADa%20Web/Parcial%202/db-replica/sync_engine.py) y coloca tus valores en `SUPABASE_URL` y `SUPABASE_KEY` (o créalos en un archivo `.env`).

---

## 3. Coordinación de Sincronización con Laptop A

Existen dos formas de conectar la aplicación de Laptop A con la réplica de Supabase:

### Opción 1: Llamada directa desde la App Flask de Laptop A (Recomendada)
Laptop A importa el motor de sincronización o realiza un POST HTTP tras guardar el pedido localmente:

```python
# En la vista de checkout / pago de Flask (Laptop A):
from db-replica.sync_engine import replicar_pedido, replicar_pago

# Después de hacer db.session.commit() local:
try:
    replicar_pedido(
        id_local=pedido.id,
        cliente_nombre=pedido.cliente,
        cliente_correo=pedido.correo,
        detalle_pedido=pedido.detalle_json,
        monto_total=pedido.total
    )
except Exception as e:
    # Si no hay internet momentáneo, la app principal sigue funcionando
    print(f"Error al sincronizar con réplica: {e}")
```

### Opción 2: Script Worker en Laptop B
Laptop B ejecuta:
```bash
python db-replica/sync_engine.py --test
```
Esto inserta un pedido y un pago de prueba con auditoría y muestra el resultado en la consola.

---

## 4. Demostración en la Sustentación del Parcial

1. **Laptop A:** Abre el navegador en `http://172.20.10.102/` y realiza un pedido con pago por Yappy.
2. **Laptop B:** Tiene abierta la pantalla de Supabase en **Table Editor** > tabla `pedidos` y `pagos`.
3. Al darle click a "Pagar" en Laptop A, en Laptop B se refresca automáticamente la tabla en Supabase mostrando el registro recibido en tiempo real.
4. **Demostración de Réplica de Solo Lectura:**
   - Intentar modificar directamente una fila con usuario no autorizado o mostrar que el nodo primario reside en el servidor web y la réplica mantiene auditoría en `sync_logs`.
