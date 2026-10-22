# 🍕 CHINOS CAFÉ S.A. — Interfaz CRUD de combos de pizza

Proyecto del **Examen Parcial 2 · Ingeniería Web (UTP)** — Prof. Napoleón Ibarra.
Parte I: aplicación web en **Python + Flask** con las secciones **Fábrica**, **Pedidos** y **Pagos**.

## ✅ Qué ya está implementado (Parte I)

| Sección | Funcionalidad |
|---|---|
| **Fábrica** | CRUD de pizzas (crear/editar/eliminar), ingredientes (mín. 2, máx. 10), refrescos, ítem adicional. ListBox/ComboBox para la selección. 6 combos precargados. |
| **Pedidos** | El cliente arma su combo. Genera **JSON** + envía **correo** (empresa/cliente). Guarda en BD local y **replica** a la 2ª BD. Calcula flete si es a domicilio. |
| **Pagos** | Confirmación de pago **YAPPY**, comprobante JSON + correo, y despacho al cliente. |
| **Extra** | Control de errores (try/except) en todas las rutas, endpoint `/api/pizzas` (JSON). |

## 🚀 Cómo correrlo

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Abrir: **http://localhost:8080**
(En el servidor Linux de las Partes II/III se expone en la IP fija, ej. `http://172.20.10.100:8080`.)

## 🗄️ Bases de datos y replicación

- **Principal:** SQLite `chinos_cafe.db` (configurable a PostgreSQL vía `DATABASE_URL`).
- **Réplica:** `chinos_cafe_replica.db` por defecto; en el examen apunta a la **BD de la VM** vía `REPLICA_DATABASE_URL` (ver `.env.example`).
- Cada pedido y pago se escribe en **ambas** BD (requisito del examen).

## 👥 División del trabajo (grupo de 2, laptops separadas)

| | **Laptop A — Desarrollo + Servidor** | **Laptop B — Red + Seguridad** |
|---|---|---|
| Parte I | App Flask, BD local, JSON, correo, Yappy | BD réplica (2ª DB) + sincronización |
| Deploy | NGINX + HTTPS + SSH/FTP + Port Knocking | — |
| Parte II | — | LAN inalámbrica, cuadro IP, Packet Tracer |
| Parte III | VM servidor NGINX (mitigación) | VM Kali (ataque): Nmap, Wireshark, pruebas |

**Flujo con Git:** cada quien trabaja en su rama y abre Pull Request.

```bash
git clone <url-del-repo>
git checkout -b feature/mi-parte
# ...trabajar...
git add . && git commit -m "mi avance"
git push origin feature/mi-parte
```

## 📂 Estructura

```
chinos-cafe/
├── app.py            # App Flask y rutas (Fábrica/Pedidos/Pagos)
├── models.py         # Modelos BD (Pizza, Ingrediente, Pedido, Pago...)
├── config.py         # Configuración (BD principal, réplica, correo)
├── utils.py          # JSON + envío de correo
├── replication.py    # Replicación a la 2ª BD
├── seed.py           # Datos iniciales (6 combos)
├── templates/        # HTML (Jinja2)
├── static/style.css  # Estilos
└── requirements.txt
```

## 📸 Para la entrega
Tomar capturas **con fecha/hora** del inicio/intermedio/final de cada parte (lo pide el examen).
