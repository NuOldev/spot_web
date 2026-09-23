from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime
from extentions import db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):

    __tablename__ = "user"
    products = db.relationship('Product')
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<User {self.user_name}>'


class Product(db.Model):

    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Numeric(7, 2), nullable=False)
    stock = db.Column(db.Integer)
    category = db.Column(db.String(50))
    add_date = db.Column(db.Date, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    def __repr__(self):
        return f'<Product {self.product_name}>'
