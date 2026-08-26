import re
from os import getenv
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
from extentions import db, bcrypt, login_manager
from models import Product, User


def create_app():
    """Create app & DB Configurations."""

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///menu.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    load_dotenv()
    app.secret_key = getenv('SECRET_KEY')

    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800
    )

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        db.create_all()

    @app.route('/')
    def inicio():
        """Muestra una página de Inicio - Bienvenida

        return: Renderización de la página de Inicio - Bienvenida.
        """

        return render_template('index.html')

    @app.route('/menu')
    def menu():

        products = {
            "especiales": Product.query.filter_by(category='especiales').all(),
            "clasicas": Product.query.filter_by(category='clasicas').all(),
            "choripanes": Product.query.filter_by(category='choripanes').all(),
            "bebidas": Product.query.filter_by(category='bebidas').all(),
            "snacks": Product.query.filter_by(category='snacks').all(),
            "postres": Product.query.filter_by(category='postres').all()
        }

        return render_template('menu.html', products=products)

    @app.route('/admin')
    @login_required
    def admin_office():

        products = current_user.products

        return render_template('admin.html', products=products)

    @app.route('/admin/new_product', methods=["GET", "POST"])
    @login_required
    def new_product():

        if request.method == "POST":

            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            price = request.form.get('price', '').strip()
            stock = request.form.get('stock', '')
            if stock == '':
                stock = 0  # Valor por defecto si está vacío
            else:
                stock = int(stock)
            category = request.form.get('category', '')

            try:
                new_product = Product(
                    product_name=name,
                    description=description,
                    price=price,
                    stock=stock,
                    category=category,
                    user_id=current_user.id)
                db.session.add(new_product)
                flash("Agregado con Éxito.")
                db.session.commit()
                print("Nuevo producto guardado correctamente")
                return redirect(url_for('new_product'))
            except TypeError as e:
                print(e)
                db.session.rollback()
                flash("Error")

        return render_template("admin_new.html")

    @app.route('/admin/edit/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def edit_product(product_id):

        product = db.get_or_404(Product, product_id,
                                description='Product not found')

        if request.method == 'POST':

            product.product_name = request.form.get('product_name').strip()
            product.description = request.form.get('description').strip()
            product.price = request.form.get('price').strip()
            product.stock = int(request.form.get('stock').strip())
            product.category = request.form.get('category')

            db.session.commit()
            return redirect(url_for('menu'))

        return render_template("admin_edit.html", product=product)

    @app.route('/admin/delete/<int:product_id>', methods=['POST'])
    @login_required
    def delete_product(product_id):

        product = db.session.get(Product, product_id)

        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('menu'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():

        if request.method == "POST":

            name = request.form.get('user_name').strip()
            password = request.form.get('password').strip()
            email = request.form.get('email').strip()

            try:
                crypt_hash = bcrypt.generate_password_hash(password)
                new_user = User(
                    user_name=name, password_hash=crypt_hash, email=email)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('admin_office'))
            except IntegrityError:
                db.session.rollback()
                flash("Error")
                return render_template('register.html')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():

        if request.method == "POST":

            email = request.form.get('email', '').strip()
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                flash("Ingresa un correo electrónico válido.", "error")
                return render_template('login.html')
            password = request.form.get('password', '').strip()

            if not email or not password:
                flash("El correo o contraseña no pueden estar vacíos!", "error")
            else:
                user: User = User.query.filter_by(email=email).first()

                if user is None:
                    flash("Este correo aún no está registrado.", "error")
                    return render_template('login.html')

                check_password = bcrypt.check_password_hash(
                    user.password_hash, password)

                if check_password:
                    flash("Acceso Correcto", "success")
                    login_user(user)
                    return redirect(url_for('admin_office'))

        return render_template('login.html')

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():

        if request.method == "POST":
            respuesta = request.form.get('salir', '').strip()

            if respuesta == '':
                return redirect(url_for('admin_office'))

            logout_user()
            return redirect(url_for('login'))

        return render_template("logout.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
