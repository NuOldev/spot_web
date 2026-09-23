from os import getenv
from sqlalchemy.exc import IntegrityError
from app import create_app
from extentions import db, bcrypt
from models import User

app = create_app()

with app.app_context():

    email = getenv("ADMIN_EMAIL")
    password = getenv("ADMIN_PASSWORD")
    name = getenv("ADMIN_NAME")

    try:
        password_hash = bcrypt.generate_password_hash(
            password).decode("utf-8")
        new_user = User(user_name=name, password_hash=password_hash,
                        email=email)
        db.session.add(new_user)
        db.session.commit()
        print("Usuario creado con éxito")
    except IntegrityError:
        db.session.rollback()
