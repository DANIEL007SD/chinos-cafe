"""Utilidades: generación de JSON, envío de correo y replicación de datos."""
import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config


def guardar_json(nombre_base, data):
    """Guarda un comprobante (pedido/pago) como archivo JSON.

    Devuelve la ruta del archivo generado.
    """
    os.makedirs(Config.JSON_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta = os.path.join(Config.JSON_DIR, f"{nombre_base}_{ts}.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return ruta


def enviar_correo(destinatarios, asunto, cuerpo, adjunto_json=None):
    """Envía un correo de confirmación.

    Si no hay servidor SMTP configurado, SIMULA el envío (imprime en consola)
    para que la aplicación funcione en el laboratorio sin credenciales reales.
    """
    if isinstance(destinatarios, str):
        destinatarios = [destinatarios]

    # Modo simulación (sin SMTP configurado)
    if not Config.SMTP_HOST:
        print("=" * 60)
        print("[CORREO SIMULADO]")
        print("Para:", ", ".join(destinatarios))
        print("Asunto:", asunto)
        print(cuerpo)
        if adjunto_json:
            print("Adjunto JSON:", adjunto_json)
        print("=" * 60)
        return True, "Correo simulado (sin SMTP configurado)"

    # Envío real por SMTP
    try:
        msg = MIMEMultipart()
        msg["From"] = Config.SMTP_USER
        msg["To"] = ", ".join(destinatarios)
        msg["Subject"] = asunto
        msg.attach(MIMEText(cuerpo, "plain"))

        if adjunto_json and os.path.exists(adjunto_json):
            with open(adjunto_json, "r", encoding="utf-8") as f:
                adj = MIMEText(f.read(), "plain")
                adj.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(adjunto_json),
                )
                msg.attach(adj)

        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASS)
            server.sendmail(Config.SMTP_USER, destinatarios, msg.as_string())
        return True, "Correo enviado"
    except Exception as e:  # control de errores (try/catch)
        return False, f"Error al enviar correo: {e}"
