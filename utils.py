"""Utilidades: generación de JSON, plantillas HTML estilo Yappy y envío de correo."""
import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config

MESES_ES = [
    "ene", "feb", "mar", "abr", "may", "jun",
    "jul", "ago", "sep", "oct", "nov", "dic"
]


def _formatear_fecha_yappy(dt=None):
    """Formatea fecha al estilo Yappy: '22 oct 2026 10:55 a. m.'"""
    if dt is None:
        dt = datetime.now()
    elif isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00")).astimezone()
        except Exception:
            dt = datetime.now()
    mes = MESES_ES[dt.month - 1]
    hora_12 = dt.strftime("%I:%M").lstrip("0") or "12:00"
    ampm = "a. m." if dt.hour < 12 else "p. m."
    return f"{dt.day} {mes} {dt.year} {hora_12} {ampm}"


def generar_html_yappy_pago(pedido: dict, pago: dict) -> str:
    """Genera el correo HTML idéntico al comprobante oficial de Yappy."""
    monto = float(pago.get("monto") or pedido.get("total") or 0)
    referencia = pago.get("referencia") or f"YAP-{pago.get('id', 100):08d}"
    fecha_str = _formatear_fecha_yappy()
    cliente = pedido.get("cliente", "Cliente")
    pizza = pedido.get("pizza", "Combo Pizza")
    refresco = pedido.get("refresco") or "Sin refresco"
    cantidad = pedido.get("cantidad", 1)
    mensaje_detalle = f"Pedido #{pedido.get('id')} · {cantidad}x {pizza} ({refresco}) - {cliente}"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>¡Enviaste un Yappy!</title>
</head>
<body style="margin:0;padding:0;background-color:#f2f6fa;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1e293b;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#f2f6fa;">
    <!-- Barra superior logo Yappy -->
    <tr>
      <td align="center" style="padding:18px 16px;background-color:#f7f9fc;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
          <tr>
            <td valign="middle" style="padding-right:8px;">
              <span style="display:inline-block;width:16px;height:16px;background-color:#00a8ff;border-radius:50%;"></span>
              <span style="display:inline-block;width:18px;height:18px;background-color:#ff7a00;border-radius:50%;margin-left:-5px;"></span>
            </td>
            <td valign="middle" style="font-size:24px;font-weight:800;color:#182b79;letter-spacing:-0.5px;">
              yappy
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- Banner Celeste + Tarjeta Blanca Superpuesta -->
    <tr>
      <td align="center" style="background:linear-gradient(180deg, #12a4ee 0%, #12a4ee 215px, #f2f6fa 215px, #f2f6fa 100%);background-color:#f2f6fa;padding:0 16px 32px 16px;">
        <!-- Cabecera Celeste -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:600px;background-color:#12a4ee;">
          <tr>
            <td align="center" style="padding:36px 20px 34px 20px;">
              <div style="font-size:19px;font-weight:700;color:#ffffff;margin-bottom:6px;">
                Enviaste por Yappy
              </div>
              <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <td valign="middle" style="font-size:32px;font-weight:800;color:#ffffff;padding-right:8px;">
                    ${monto:.2f}
                  </td>
                  <td valign="middle">
                    <span style="display:inline-block;width:24px;height:24px;line-height:24px;text-align:center;background-color:#16a34a;color:#ffffff;border-radius:50%;font-size:14px;font-weight:bold;">
                      &#10003;
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        <!-- Tarjeta Blanca Central -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:430px;background-color:#ffffff;border-radius:16px;box-shadow:0 6px 24px rgba(15,23,42,0.08);">
          <tr>
            <td style="padding:32px 32px 28px 32px;">
              <!-- Enviado a -->
              <div style="text-align:center;font-size:13px;color:#64748b;margin-bottom:10px;">
                Enviado a
              </div>
              <div style="text-align:center;font-size:19px;font-weight:700;color:#334155;margin-bottom:10px;">
                CHINOS CAFÉ S.A.
              </div>
              <div style="text-align:center;font-size:13px;font-weight:600;color:#475569;margin-bottom:30px;">
                &#128241; 6800-2026 &middot; Cliente: {cliente}
              </div>

              <!-- Fila: Fecha -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom:1px solid #e2e8f0;padding-bottom:12px;margin-bottom:14px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">
                    Fecha
                  </td>
                  <td align="right" style="font-size:13px;font-weight:700;color:#334155;">
                    {fecha_str}
                  </td>
                  <td align="right" width="26" style="font-size:15px;color:#475569;">
                    &#128197;
                  </td>
                </tr>
              </table>

              <!-- Fila: Mensaje -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom:1px solid #e2e8f0;padding-bottom:12px;margin-bottom:14px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">
                    Mensaje
                  </td>
                  <td align="right" style="font-size:13px;font-weight:600;color:#334155;">
                    {mensaje_detalle}
                  </td>
                  <td align="right" width="26" style="font-size:15px;color:#475569;">
                    &#128172;
                  </td>
                </tr>
              </table>

              <!-- Fila: Confirmación -->
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="padding-bottom:4px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">
                    Confirmación
                  </td>
                  <td align="right" style="font-size:13px;font-weight:700;color:#1e293b;letter-spacing:0.3px;">
                    {referencia}
                  </td>
                  <td align="right" width="26" style="font-size:15px;color:#475569;">
                    &#129534;
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- Pie de página -->
    <tr>
      <td align="center" style="padding:8px 16px 40px 16px;background-color:#f2f6fa;">
        <p style="margin:0;font-size:13px;color:#475569;line-height:1.5;">
          Estamos aquí para ayudarte. Visita nuestra sección de<br>
          <a href="#" style="color:#0284c7;font-weight:700;text-decoration:none;">preguntas frecuentes</a> para más información.
        </p>
      </td>
    </tr>
  </table>
</body>
</html>"""


def generar_html_yappy_pedido(pedido: dict) -> str:
    """Genera un comprobante HTML de pedido registrado con estética Yappy Comercial."""
    monto = float(pedido.get("total") or 0)
    fecha_str = _formatear_fecha_yappy()
    cliente = pedido.get("cliente", "Cliente")
    pizza = pedido.get("pizza", "Combo Pizza")
    refresco = pedido.get("refresco") or "Sin refresco"
    cantidad = pedido.get("cantidad", 1)
    entrega = "Retiro en sitio" if pedido.get("retiro_en_sitio") else "Entrega a domicilio (+Flete)"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Pedido Registrado - CHINOS CAFÉ S.A.</title>
</head>
<body style="margin:0;padding:0;background-color:#f2f6fa;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1e293b;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#f2f6fa;">
    <tr>
      <td align="center" style="padding:18px 16px;background-color:#f7f9fc;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0">
          <tr>
            <td valign="middle" style="padding-right:8px;">
              <span style="display:inline-block;width:16px;height:16px;background-color:#00a8ff;border-radius:50%;"></span>
              <span style="display:inline-block;width:18px;height:18px;background-color:#ff7a00;border-radius:50%;margin-left:-5px;"></span>
            </td>
            <td valign="middle" style="font-size:24px;font-weight:800;color:#182b79;">
              yappy <span style="font-weight:400;font-size:15px;color:#64748b;">comercial</span>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td align="center" style="background:linear-gradient(180deg, #12a4ee 0%, #12a4ee 215px, #f2f6fa 215px, #f2f6fa 100%);background-color:#f2f6fa;padding:0 16px 32px 16px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:600px;background-color:#12a4ee;">
          <tr>
            <td align="center" style="padding:36px 20px 34px 20px;">
              <div style="font-size:19px;font-weight:700;color:#ffffff;margin-bottom:6px;">
                Orden Pendiente de Pago #{pedido.get('id')}
              </div>
              <div style="font-size:32px;font-weight:800;color:#ffffff;">
                ${monto:.2f}
              </div>
            </td>
          </tr>
        </table>
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:430px;background-color:#ffffff;border-radius:16px;box-shadow:0 6px 24px rgba(15,23,42,0.08);">
          <tr>
            <td style="padding:32px 32px 28px 32px;">
              <div style="text-align:center;font-size:13px;color:#64748b;margin-bottom:8px;">Comercio</div>
              <div style="text-align:center;font-size:19px;font-weight:700;color:#334155;margin-bottom:24px;">CHINOS CAFÉ S.A.</div>

              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom:1px solid #e2e8f0;padding-bottom:12px;margin-bottom:14px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">Cliente</td>
                  <td align="right" style="font-size:13px;font-weight:700;color:#334155;">{cliente}</td>
                </tr>
              </table>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom:1px solid #e2e8f0;padding-bottom:12px;margin-bottom:14px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">Combo</td>
                  <td align="right" style="font-size:13px;font-weight:700;color:#334155;">{cantidad}x {pizza} + {refresco}</td>
                </tr>
              </table>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-bottom:1px solid #e2e8f0;padding-bottom:12px;margin-bottom:14px;">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">Modalidad</td>
                  <td align="right" style="font-size:13px;font-weight:600;color:#334155;">{entrega}</td>
                </tr>
              </table>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <td align="left" style="font-size:13px;color:#64748b;">Fecha</td>
                  <td align="right" style="font-size:13px;font-weight:700;color:#334155;">{fecha_str}</td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


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


def enviar_correo(destinatarios, asunto, cuerpo, adjunto_json=None, cuerpo_html=None):
    """Envía un correo de confirmación (soporta diseño HTML estilo Yappy + JSON adjunto).

    Si no hay servidor SMTP configurado, SIMULA el envío (imprime en consola)
    para que la aplicación funcione en el laboratorio sin credenciales reales.
    """
    if isinstance(destinatarios, str):
        destinatarios = [destinatarios]
    # Eliminar duplicados manteniendo el orden
    destinatarios = list(dict.fromkeys(d for d in destinatarios if d))

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
        msg = MIMEMultipart("mixed")
        msg["From"] = f"Yappy Comercial - Chinos Café <{Config.SMTP_USER}>"
        msg["To"] = ", ".join(destinatarios)
        msg["Subject"] = asunto

        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(cuerpo, "plain", "utf-8"))
        if cuerpo_html:
            alt.attach(MIMEText(cuerpo_html, "html", "utf-8"))
        msg.attach(alt)

        if adjunto_json and os.path.exists(adjunto_json):
            with open(adjunto_json, "r", encoding="utf-8") as f:
                adj = MIMEText(f.read(), "plain", "utf-8")
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
