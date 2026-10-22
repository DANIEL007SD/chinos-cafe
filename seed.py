"""Datos iniciales (semilla): ingredientes, refrescos y 5 combos de pizza.

El examen exige "mínimo 5 combos de PIZZA por Sitio WEB".
"""
from models import db, Ingrediente, Refresco, Pizza


def cargar_datos():
    if Pizza.query.count() > 0:
        return  # ya cargado

    ingredientes = [
        "Queso", "Peperoni", "Jamón", "Piña", "Champiñón", "Pimiento",
        "Cebolla", "Tocino", "Pollo", "Aceitunas", "Maíz", "Salchicha",
    ]
    ing_obj = {}
    for n in ingredientes:
        o = Ingrediente(nombre=n)
        db.session.add(o)
        ing_obj[n] = o

    refrescos = [("Coca-Cola", 1.25), ("Sprite", 1.25), ("Fanta", 1.25),
                 ("Agua", 0.75), ("Chicha", 1.00)]
    for n, p in refrescos:
        db.session.add(Refresco(nombre=n, precio=p))

    db.session.commit()

    combos = [
        ("Combo Clásica", 7.50, ["Queso", "Peperoni"], "Pan de ajo"),
        ("Combo Hawaiana", 8.00, ["Queso", "Jamón", "Piña"], "Salsa BBQ"),
        ("Combo Vegetariana", 7.75, ["Queso", "Champiñón", "Pimiento", "Cebolla", "Maíz"], "Ensalada"),
        ("Combo Carnívora", 9.50, ["Queso", "Peperoni", "Tocino", "Salchicha", "Pollo"], "Alitas (4)"),
        ("Combo Suprema", 10.00, ["Queso", "Peperoni", "Champiñón", "Pimiento", "Cebolla", "Aceitunas", "Jamón"], "Postre"),
        ("Combo Pollo BBQ", 9.00, ["Queso", "Pollo", "Cebolla", "Maíz"], "Dip BBQ"),
    ]
    for nombre, precio, ings, adicional in combos:
        pizza = Pizza(nombre=nombre, precio=precio, item_adicional=adicional)
        pizza.ingredientes = [ing_obj[i] for i in ings]
        db.session.add(pizza)

    db.session.commit()
