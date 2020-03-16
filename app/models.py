from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_name = db.Column(db.String(64), index=True)
    price = db.Column(db.Integer, index=True)
    description = db.Column(db.String(300))
    category = db.Column(db.String(20))
    item = db.Column(db.String(200))
    sku = db.Column(db.String(200))
    size = db.Column(db.Integer, index=True, unique=False)
    size_number = db.Column(db.Integer, index=True, unique=False)
    reviews = db.Column(db.String(64), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    image = db.Column(db.String(64), index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Product {}>'.format(self.title)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    image = db.Column(db.String(200))
    title = db.Column(db.String(64), index=True)
    price = db.Column(db.Integer, index=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(64), index=True)
    amount = db.Column(db.Integer)
    # date
    qty = db.Column(db.Integer, index=True)





