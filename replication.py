"""Replicación de datos hacia la segunda BD (Supabase / PostgreSQL / VM).

Requisito del examen (Parte I - PEDIDOS):
  "Replicación de los datos en otra DB (Relacional-Máquina Virtual).
   La data debe estar en ambas (2) DB."

Soporta:
1. Supabase REST API (usando SUPABASE_URL y SUPABASE_SECRET_KEY / SUPABASE_PUBLISHABLE_KEY).
2. PostgreSQL directo (vía REPLICA_DATABASE_URL con ON CONFLICT).
3. SQLite local de respaldo (por defecto).
"""
import json
import urllib.error
import urllib.request
from sqlalchemy import create_engine, text

from config import Config

_engine = create_engine(Config.REPLICA_DATABASE_URL)
_is_postgres = Config.REPLICA_DATABASE_URL.startswith("postgresql")


def _init():
    """Crea las tablas réplica en el motor SQLAlchemy si está activo."""
    try:
        with _engine.begin() as conn:
            conn.execute(text(
                """CREATE TABLE IF NOT EXISTS pedido_replica (
                    id INTEGER PRIMARY KEY,
                    cliente TEXT, correo_cliente TEXT, pizza TEXT,
                    refresco TEXT, cantidad INTEGER, retiro_en_sitio INTEGER,
                    total REAL, estado TEXT, fecha TEXT
                )"""
            ))
            conn.execute(text(
                """CREATE TABLE IF NOT EXISTS pago_replica (
                    id INTEGER PRIMARY KEY,
                    pedido_id INTEGER, metodo TEXT, referencia TEXT,
                    monto REAL, fecha TEXT
                )"""
            ))
    except Exception as e:
        print(f"[Aviso] No se pudo inicializar tabla SQL local/remota: {e}")


def _supabase_upsert(tabla: str, payload: dict) -> tuple[bool, str]:
    """Envía un registro a Supabase mediante su API REST (PostgREST)."""
    url = f"{Config.SUPABASE_URL}/rest/v1/{tabla}"
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "apikey": Config.SUPABASE_KEY,
        "Authorization": f"Bearer {Config.SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True, f"Sincronizado en Supabase ({tabla}, HTTP {resp.status})"
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", errors="ignore")
        return False, f"Error Supabase HTTP {e.code}: {detalle}"
    except Exception as e:
        return False, f"Error de conexión a Supabase: {e}"


def replicar_pedido(d):
    """Copia un pedido a la BD réplica (Supabase y/o SQLAlchemy). Devuelve (ok, mensaje)."""
    fila = {
        "id": d["id"],
        "cliente": d["cliente"],
        "correo_cliente": d["correo_cliente"],
        "pizza": d["pizza"],
        "refresco": d["refresco"],
        "cantidad": d["cantidad"],
        "retiro_en_sitio": 1 if d["retiro_en_sitio"] else 0,
        "total": d["total"],
        "estado": d["estado"],
        "fecha": d["fecha"],
    }

    # 1. Si está configurado Supabase REST API, replicar hacia la nube
    if Config.SUPABASE_URL and Config.SUPABASE_KEY and "tu-proyecto" not in Config.SUPABASE_URL:
        ok_sb, msg_sb = _supabase_upsert("pedido_replica", fila)
        if not ok_sb:
            return False, msg_sb
        # También guardar en el motor local de respaldo
        try:
            _guardar_pedido_sql(fila)
        except Exception:
            pass
        return True, "Pedido replicado en la 2ª DB (Supabase)"

    # 2. Motor SQLAlchemy (PostgreSQL o SQLite)
    try:
        _guardar_pedido_sql(fila)
        return True, "Pedido replicado en la 2ª DB"
    except Exception as e:  # control de errores
        return False, f"Error de replicación (pedido): {e}"


def _guardar_pedido_sql(fila: dict):
    with _engine.begin() as conn:
        if _is_postgres:
            conn.execute(
                text(
                    """INSERT INTO pedido_replica
                    (id, cliente, correo_cliente, pizza, refresco, cantidad,
                     retiro_en_sitio, total, estado, fecha)
                    VALUES (:id, :cliente, :correo_cliente, :pizza, :refresco,
                     :cantidad, :retiro_en_sitio, :total, :estado, :fecha)
                    ON CONFLICT (id) DO UPDATE SET
                        estado = EXCLUDED.estado,
                        total = EXCLUDED.total"""
                ),
                fila,
            )
        else:
            conn.execute(
                text(
                    """INSERT OR REPLACE INTO pedido_replica
                    (id, cliente, correo_cliente, pizza, refresco, cantidad,
                     retiro_en_sitio, total, estado, fecha)
                    VALUES (:id, :cliente, :correo_cliente, :pizza, :refresco,
                     :cantidad, :retiro_en_sitio, :total, :estado, :fecha)"""
                ),
                fila,
            )


def replicar_pago(d):
    """Copia un pago a la BD réplica (Supabase y/o SQLAlchemy). Devuelve (ok, mensaje)."""
    # 1. Si está configurado Supabase REST API, replicar hacia la nube
    if Config.SUPABASE_URL and Config.SUPABASE_KEY and "tu-proyecto" not in Config.SUPABASE_URL:
        ok_sb, msg_sb = _supabase_upsert("pago_replica", d)
        if not ok_sb:
            return False, msg_sb
        try:
            _guardar_pago_sql(d)
        except Exception:
            pass
        return True, "Pago replicado en la 2ª DB (Supabase)"

    # 2. Motor SQLAlchemy (PostgreSQL o SQLite)
    try:
        _guardar_pago_sql(d)
        return True, "Pago replicado en la 2ª DB"
    except Exception as e:
        return False, f"Error de replicación (pago): {e}"


def _guardar_pago_sql(d: dict):
    with _engine.begin() as conn:
        if _is_postgres:
            conn.execute(
                text(
                    """INSERT INTO pago_replica
                    (id, pedido_id, metodo, referencia, monto, fecha)
                    VALUES (:id, :pedido_id, :metodo, :referencia, :monto, :fecha)
                    ON CONFLICT (id) DO UPDATE SET
                        referencia = EXCLUDED.referencia,
                        monto = EXCLUDED.monto"""
                ),
                d,
            )
        else:
            conn.execute(
                text(
                    """INSERT OR REPLACE INTO pago_replica
                    (id, pedido_id, metodo, referencia, monto, fecha)
                    VALUES (:id, :pedido_id, :metodo, :referencia, :monto, :fecha)"""
                ),
                d,
            )


_init()
