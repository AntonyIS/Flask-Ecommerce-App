from flask import render_template, url_for, flash, redirect,session, request
from app.forms import LoginForm, RegistrationForm, ProductForm
from app import app
from flask_login import current_user, login_user,logout_user, login_required

from app.models import User,Product,Cart,Order
from app import db



@app.route('/')
@app.route('/home')
def index():
    form = LoginForm()
    products = Product.query.all()[:4]
    try:
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        return render_template('index.html', title='Home page', form=form, products=products, cart_count=len(carts))
    except KeyError:
        form = LoginForm()
        return render_template('index.html', title='Home page', form=form, products=products)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))

        if user.email =='a@gmail.com':
            session['admin'] = True
            session['user_id'] = user.id

            login_user(user, remember=form.remember_me.data)
        session['user_id'] = user.id

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('signup.html', title='Register', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if session['admin'] == True :
        products = Product.query.all()
        orders = Order.query.all()
        form = ProductForm()
        if request.method == 'POST':
            product = Product(title=form.title.data,price=form.price.data, description=form.description.data,size=form.size.data,category=form.category.data)
            db.session.add(product)
            db.session.commit()
            flash('Congratulations, you {}'.format(form.title.data))
            return redirect(url_for('dashboard'))
        else:
            return render_template('dashboard.html', form=form, products=products, orders=orders)
    else:
        return render_template('index.html')


@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    form = LoginForm()
    return render_template('product_detail.html', product=product, form=form)


@app.route('/add/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    cart = Cart(product_id=product_id, user_id=session['user_id'], title=product.title, price=product.price)

    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/shopping-cart')
def shopping_cart():
    try:
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        total = 0
        for cart in carts:
            total += cart.price
        return render_template('shopping_cart.html', title='Home page', cart_count=len(carts),carts=carts, total=total)
    except KeyError:
        return redirect(url_for('index'))


@app.route('/remove/<int:cart_id>')
def remove(cart_id):
    cart = Cart.query.get(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('shopping_cart'))


@app.route('/checkout')
@login_required
def checkout():
    try:
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        user = User.query.get(session['user_id'])
        total = 0
        cart_count =len(carts)
        for cart in carts:
            total += cart.price
        order = Order(user_id=session['user_id'],amount=total,qty=cart_count, userame=user.username)
        db.session.add(order)
        db.session.commit()
        count = 0
        while count < cart_count:

            db.session.delete(carts[count])
            db.session.commit()
            count += 1
        return redirect(url_for('checkedout'))
    except KeyError:
        return redirect(url_for('index'))


@app.route('/checked-out')
@login_required
def checkedout():
    return render_template('checkout.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user_id', None)
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('feedback.html', error=error, title='Antony Injila | 404'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('feedback.html', error=error), 500