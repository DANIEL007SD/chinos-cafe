"""Configuración de la aplicación CHINOS CAFÉ S.A.

Centraliza las variables que cambian entre la laptop A (desarrollo/servidor)
y la laptop B (réplica). Cada integrante ajusta su .env o estas variables.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chinos-cafe-dev-key")

    # --- Base de datos PRINCIPAL (local relacional) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "chinos_cafe.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Base de datos RÉPLICA (otra máquina / VM) ---
    # Parte I del examen: "La data debe estar en ambas (2) DB".
    # Ejemplo para PostgreSQL en la VM:  postgresql://user:pass@172.20.10.150:5432/chinos
    REPLICA_DATABASE_URL = os.environ.get(
        "REPLICA_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "chinos_cafe_replica.db"),
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
