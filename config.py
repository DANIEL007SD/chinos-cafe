"""Configuración de la aplicación CHINOS CAFÉ S.A.

Centraliza las variables que cambian entre la laptop A (desarrollo/servidor)
y la laptop B (réplica). Cada integrante ajusta su .env o estas variables.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Cargar variables de .env automáticamente si existe el archivo
_env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(_env_path):
    with open(_env_path, encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))


def _clean_supabase_url(raw_url: str) -> str:
    url = raw_url.strip().rstrip("/")
    if url.endswith("/rest/v1"):
        url = url[: -len("/rest/v1")]
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chinos-cafe-dev-key")

    # --- Base de datos PRINCIPAL (local relacional) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "chinos_cafe.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Base de datos RÉPLICA (otra máquina / VM / Supabase) ---
    # Parte I del examen: "La data debe estar en ambas (2) DB".
    # Ejemplo para PostgreSQL en la VM o Supabase:  postgresql://user:pass@172.20.10.150:5432/chinos
    REPLICA_DATABASE_URL = os.environ.get(
        "REPLICA_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "chinos_cafe_replica.db"),
    )

    # --- Credenciales Supabase REST API (Laptop B) ---
    SUPABASE_URL = _clean_supabase_url(os.environ.get("SUPABASE_URL", ""))
    SUPABASE_PUBLISHABLE_KEY = os.environ.get("SUPABASE_PUBLISHABLE_KEY", "")
    SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY") or os.environ.get(
        "SUPABASE_PUBLISHABLE_KEY", ""
    )

    # --- Correo (confirmaciones de pedido y pago) ---
    # Si no se configura un servidor SMTP, el envío se simula y se guarda el JSON.
    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASS = os.environ.get("SMTP_PASS", "")
    MAIL_EMPRESA = os.environ.get("MAIL_EMPRESA", "chinoscafe@example.com")

    # Carpeta donde se guardan los archivos JSON de pedidos/pagos
    JSON_DIR = os.path.join(BASE_DIR, "comprobantes")

    # Flete sugerido si el cliente no pasa a retiro en sitio
    FLETE = float(os.environ.get("FLETE", "3.50"))
