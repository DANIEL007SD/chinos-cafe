"""CHINOS CAFÉ S.A. - Interfaz CRUD de combos de pizza (Flask).

Examen Parcial 2 - Ingeniería Web (UTP).
Parte I: secciones FÁBRICA, PEDIDOS y PAGOS.
"""
from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify
)

from config import Config
from models import db, Ingrediente, Refresco, Pizza, Pedido, Pago
from utils import (
    guardar_json,
    enviar_correo,
    generar_html_yappy_pedido,
    generar_html_yappy_pago,
)
from replication import replicar_pedido, replicar_pago


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        from seed import cargar_datos
        cargar_datos()

    # ------------------------- INICIO -------------------------
    @app.route("/")
    def index():
        return render_template("index.html")

    # ------------------------- FÁBRICA ------------------------
    # Registrar / crear / actualizar / eliminar pizzas (CRUD).
    @app.route("/fabrica")
    def fabrica():
        pizzas = Pizza.query.all()
        ingredientes = Ingrediente.query.all()
        return render_template("fabrica.html", pizzas=pizzas, ingredientes=ingredientes)

    @app.route("/fabrica/crear", methods=["POST"])
    def fabrica_crear():
        try:
            nombre = request.form["nombre"].strip()
            precio = float(request.form.get("precio", 0) or 0)
            item_adicional = request.form.get("item_adicional", "").strip()
            ids = request.form.getlist("ingredientes")

            # Regla del examen: mínimo 2, máximo 10 ingredientes.
            if not (2 <= len(ids) <= 10):
                flash("Una pizza debe tener entre 2 y 10 ingredientes.", "error")
                return redirect(url_for("fabrica"))

            pizza = Pizza(nombre=nombre, precio=precio, item_adicional=item_adicional)
            pizza.ingredientes = Ingrediente.query.filter(Ingrediente.id.in_(ids)).all()
            db.session.add(pizza)
            db.session.commit()
            flash(f"Pizza '{nombre}' creada.", "ok")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear la pizza: {e}", "error")
        return redirect(url_for("fabrica"))

    @app.route("/fabrica/actualizar/<int:pid>", methods=["POST"])
    def fabrica_actualizar(pid):
        try:
            pizza = Pizza.query.get_or_404(pid)
            pizza.nombre = request.form["nombre"].strip()
            pizza.precio = float(request.form.get("precio", 0) or 0)
            pizza.item_adicional = request.form.get("item_adicional", "").strip()
            ids = request.form.getlist("ingredientes")
            if ids:
                if not (2 <= len(ids) <= 10):
                    flash("Una pizza debe tener entre 2 y 10 ingredientes.", "error")
                    return redirect(url_for("fabrica"))
                pizza.ingredientes = Ingrediente.query.filter(Ingrediente.id.in_(ids)).all()
            db.session.commit()
            flash("Pizza actualizada.", "ok")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar: {e}", "error")
        return redirect(url_for("fabrica"))

    @app.route("/fabrica/eliminar/<int:pid>", methods=["POST"])
    def fabrica_eliminar(pid):
        try:
            pizza = Pizza.query.get_or_404(pid)
            db.session.delete(pizza)
            db.session.commit()
            flash("Pizza eliminada.", "ok")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al eliminar: {e}", "error")
        return redirect(url_for("fabrica"))

    # ------------------------- PEDIDOS ------------------------
    @app.route("/pedidos")
    def pedidos():
        pizzas = Pizza.query.all()
        refrescos = Refresco.query.all()
        lista = Pedido.query.order_by(Pedido.fecha.desc()).all()
        return render_template(
            "pedidos.html", pizzas=pizzas, refrescos=refrescos, pedidos=lista
        )

    @app.route("/pedidos/crear", methods=["POST"])
    def pedidos_crear():
        try:
            cliente = request.form["cliente"].strip()
            correo = request.form["correo_cliente"].strip()
            pizza = Pizza.query.get_or_404(int(request.form["pizza_id"]))
            refresco_id = request.form.get("refresco_id")
            refresco = Refresco.query.get(int(refresco_id)) if refresco_id else None
            cantidad = max(1, int(request.form.get("cantidad", 1)))
            retiro = request.form.get("retiro_en_sitio") == "si"

            total = pizza.precio * cantidad
            if refresco:
                total += refresco.precio * cantidad
            if not retiro:
                total += Config.FLETE  # flete sugerido

            pedido = Pedido(
                cliente=cliente, correo_cliente=correo, pizza_id=pizza.id,
                refresco_id=refresco.id if refresco else None,
                cantidad=cantidad, retiro_en_sitio=retiro, total=total,
            )
            db.session.add(pedido)
            db.session.commit()

            # Comprobante JSON + correo (empresa, cliente, operario)
            data = pedido.to_dict()
            ruta = guardar_json("pedido", data)
            enviar_correo(
                [Config.MAIL_EMPRESA, correo],
                f"Pedido #{pedido.id} recibido - CHINOS CAFÉ",
                f"Hola {cliente}, tu pedido fue registrado.\n\n{data}",
                adjunto_json=ruta,
                cuerpo_html=generar_html_yappy_pedido(data),
            )

            # Replicación a la 2ª DB
            ok, msg = replicar_pedido(data)
            flash(f"Pedido #{pedido.id} creado. {msg}", "ok" if ok else "error")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear el pedido: {e}", "error")
        return redirect(url_for("pedidos"))

    # ------------------------- PAGOS --------------------------
    @app.route("/pagos")
    def pagos():
        pendientes = Pedido.query.filter(Pedido.estado == "PENDIENTE").all()
        lista = Pago.query.order_by(Pago.fecha.desc()).all()
        return render_template("pagos.html", pendientes=pendientes, pagos=lista)

    @app.route("/pagos/confirmar", methods=["POST"])
    def pagos_confirmar():
        try:
            pedido = Pedido.query.get_or_404(int(request.form["pedido_id"]))
            referencia = request.form.get("referencia", "").strip()

            pago = Pago(
                pedido_id=pedido.id, metodo="YAPPY",
                referencia=referencia, monto=pedido.total,
            )
            pedido.estado = "PAGADO"
            db.session.add(pago)
            db.session.commit()

            # Comprobante JSON + correo de confirmación de pago
            data = pago.to_dict()
            pedido_dict = pedido.to_dict()
            ruta = guardar_json("pago", data)
            enviar_correo(
                [Config.MAIL_EMPRESA, pedido.correo_cliente],
                f"¡Enviaste un Yappy! 💸 - Pedido #{pedido.id}",
                f"Pago recibido vía YAPPY. Ref: {referencia}. "
                f"El pedido pasa a despacho.\n\n{data}",
                adjunto_json=ruta,
                cuerpo_html=generar_html_yappy_pago(pedido_dict, data),
            )

            # Replicación a la 2ª DB (actualizar estado del pedido y registrar pago)
            replicar_pedido(pedido_dict)
            ok, msg = replicar_pago(data)
            flash(f"Pago del pedido #{pedido.id} confirmado. {msg}",
                  "ok" if ok else "error")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al confirmar el pago: {e}", "error")
        return redirect(url_for("pagos"))

    @app.route("/pagos/despachar/<int:pid>", methods=["POST"])
    def pagos_despachar(pid):
        try:
            pedido = Pedido.query.get_or_404(pid)
            pedido.estado = "DESPACHADO"
            db.session.commit()
            replicar_pedido(pedido.to_dict())
            flash(f"Pedido #{pid} despachado al cliente.", "ok")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al despachar: {e}", "error")
        return redirect(url_for("pagos"))

    # ------------------------- API JSON -----------------------
    @app.route("/api/pizzas")
    def api_pizzas():
        return jsonify([p.to_dict() for p in Pizza.query.all()])

    return app


if __name__ == "__main__":
    import os
    import socket

    app = create_app()
    port = int(os.environ.get("PORT", 8080))
    # Si el puerto 8080 está ocupado en Windows (ej. por Apache httpd), usar 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", port)) == 0:
            port = 5000
    # 0.0.0.0 para que la laptop B (red LAN) pueda acceder al servidor.
    app.run(host="0.0.0.0", port=port, debug=True)
