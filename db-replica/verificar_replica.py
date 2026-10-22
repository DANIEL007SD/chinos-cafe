"""Script de prueba para verificar que la replicación hacia Supabase funciona."""
from datetime import datetime, timezone
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config
from replication import replicar_pedido, replicar_pago


def probar_sincronizacion():
    print("=== Prueba de Replicación CHINOS CAFÉ S.A. ===")
    print(f"SUPABASE_URL: {Config.SUPABASE_URL}")

    if not Config.SUPABASE_URL or "tu-proyecto" in Config.SUPABASE_URL:
        print(
            "[!] Falta colocar tu Project URL real en el archivo .env:\n"
            "    SUPABASE_URL=https://<id-de-tu-proyecto>.supabase.co"
        )
        return

    ahora = datetime.now(timezone.utc).isoformat()

    pedido_demo = {
        "id": 999,
        "cliente": "Cliente Prueba Supabase",
        "correo_cliente": "prueba@chinoscafe.com",
        "pizza": "Combo Especial Chinos",
        "refresco": "Coca-Cola",
        "cantidad": 2,
        "retiro_en_sitio": False,
        "total": 23.50,
        "estado": "PAGADO",
        "fecha": ahora,
    }

    ok_ped, msg_ped = replicar_pedido(pedido_demo)
    print(f"Resultado Pedido: ok={ok_ped} | {msg_ped}")

    pago_demo = {
        "id": 999,
        "pedido_id": 999,
        "metodo": "YAPPY",
        "referencia": "YAPPY-TEST-001",
        "monto": 23.50,
        "fecha": ahora,
    }

    ok_pag, msg_pag = replicar_pago(pago_demo)
    print(f"Resultado Pago:   ok={ok_pag} | {msg_pag}")

    if not ok_ped and "PGRST205" in msg_ped:
        print(
            "\n[!] Las credenciales y conexión a Supabase funcionan, pero aún no existen las tablas.\n"
            "    Abre el SQL Editor de tu proyecto en:\n"
            "    https://supabase.com/dashboard/project/talewwtbjoyfsoresvmx/sql/new\n"
            "    Pega el contenido de 'db-replica/schema_supabase.sql' y presiona 'Run'."
        )


if __name__ == "__main__":
    probar_sincronizacion()
