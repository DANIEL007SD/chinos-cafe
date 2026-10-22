"""Replicación de datos hacia la segunda BD (otra máquina / VM).

Requisito del examen (Parte I - PEDIDOS):
  "Replicación de los datos en otra DB (Relacional-Máquina Virtual).
   La data debe estar en ambas (2) DB."

Implementación sencilla y portable: se abre un segundo motor SQLAlchemy
apuntando a la BD réplica (REPLICA_DATABASE_URL) y se copia cada pedido/pago.
Funciona con SQLite (por defecto) o con PostgreSQL/MySQL en la VM.
"""
from sqlalchemy import create_engine, text

from config import Config

_engine = create_engine(Config.REPLICA_DATABASE_URL)


def _init():
    """Crea las tablas réplica si no existen."""
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


def replicar_pedido(d):
    """Copia un pedido a la BD réplica. Devuelve (ok, mensaje)."""
    try:
        with _engine.begin() as conn:
            conn.execute(
                text(
                    """INSERT OR REPLACE INTO pedido_replica
                    (id, cliente, correo_cliente, pizza, refresco, cantidad,
                     retiro_en_sitio, total, estado, fecha)
                    VALUES (:id, :cliente, :correo_cliente, :pizza, :refresco,
                     :cantidad, :retiro_en_sitio, :total, :estado, :fecha)"""
                ),
                {
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
                },
            )
        return True, "Pedido replicado en la 2ª DB"
    except Exception as e:  # control de errores
        return False, f"Error de replicación (pedido): {e}"


def replicar_pago(d):
    """Copia un pago a la BD réplica. Devuelve (ok, mensaje)."""
    try:
        with _engine.begin() as conn:
            conn.execute(
                text(
                    """INSERT OR REPLACE INTO pago_replica
                    (id, pedido_id, metodo, referencia, monto, fecha)
                    VALUES (:id, :pedido_id, :metodo, :referencia, :monto, :fecha)"""
                ),
                d,
            )
        return True, "Pago replicado en la 2ª DB"
    except Exception as e:
        return False, f"Error de replicación (pago): {e}"


_init()
