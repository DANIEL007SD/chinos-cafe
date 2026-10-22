"""Modelos de datos (BD relacional) de CHINOS CAFÉ S.A."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Tabla intermedia Pizza <-> Ingrediente (muchos a muchos)
pizza_ingredientes = db.Table(
    "pizza_ingredientes",
    db.Column("pizza_id", db.Integer, db.ForeignKey("pizza.id"), primary_key=True),
    db.Column("ingrediente_id", db.Integer, db.ForeignKey("ingrediente.id"), primary_key=True),
)


class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False, unique=True)

    def __repr__(self):
        return self.nombre


class Refresco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False, unique=True)
    precio = db.Column(db.Float, default=0.0)


class Pizza(db.Model):
    """Combo de pizza creado en la sección FÁBRICA.

    Reglas del examen: mínimo 2, máximo 10 ingredientes por pizza.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    precio = db.Column(db.Float, nullable=False, default=0.0)
    item_adicional = db.Column(db.String(80), default="")
    ingredientes = db.relationship(
        "Ingrediente", secondary=pizza_ingredientes, backref="pizzas"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "item_adicional": self.item_adicional,
            "ingredientes": [i.nombre for i in self.ingredientes],
        }


class Pedido(db.Model):
    """Sección PEDIDOS: el cliente arma su combo."""
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(120), nullable=False)
    correo_cliente = db.Column(db.String(120), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizza.id"), nullable=False)
    refresco_id = db.Column(db.Integer, db.ForeignKey("refresco.id"))
    cantidad = db.Column(db.Integer, default=1)
    retiro_en_sitio = db.Column(db.Boolean, default=True)
    total = db.Column(db.Float, default=0.0)
    estado = db.Column(db.String(30), default="PENDIENTE")  # PENDIENTE/PAGADO/DESPACHADO
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    pizza = db.relationship("Pizza")
    refresco = db.relationship("Refresco")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente,
            "correo_cliente": self.correo_cliente,
            "pizza": self.pizza.nombre if self.pizza else None,
            "refresco": self.refresco.nombre if self.refresco else None,
            "cantidad": self.cantidad,
            "retiro_en_sitio": self.retiro_en_sitio,
            "total": self.total,
            "estado": self.estado,
            "fecha": self.fecha.isoformat(),
        }


class Pago(db.Model):
    """Sección PAGOS: confirmación del pago (Yappy Comercial)."""
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    metodo = db.Column(db.String(40), default="YAPPY")
    referencia = db.Column(db.String(80))
    monto = db.Column(db.Float, default=0.0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    pedido = db.relationship("Pedido")

    def to_dict(self):
        return {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "metodo": self.metodo,
            "referencia": self.referencia,
            "monto": self.monto,
            "fecha": self.fecha.isoformat(),
        }
