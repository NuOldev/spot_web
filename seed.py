import json
from extentions import db
from models import Product, User
from app import create_app


app = create_app()

with app.app_context():

    admin = User.query.filter_by(user_name="James").first()

    if not admin:
        print("Admin no encontrado, corre primero crear_admin.py")
    else:
        with open('data/menu.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for k, v in data.items():
            for val in v:

                nombre = val["nombre_menu"]
                descripcion = val["descripcion"]
                precio = val["precio"]
                categoria = val["categoria"]
                stock = val["stock"]

                existe = Product.query.filter_by(
                    product_name=nombre, user_id=admin.id).first()

                if existe:
                    continue

                nuevo = Product(
                    product_name=nombre,
                    description=descripcion,
                    price=precio,
                    stock=stock,
                    category=categoria,
                    user_id=admin.id
                )
                db.session.add(nuevo)

    db.session.commit()
    print("Seed completado.")
