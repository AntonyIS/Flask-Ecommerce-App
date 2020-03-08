from flask import render_template, url_for, flash, redirect,session, request
from werkzeug.utils import secure_filename

from app.forms import LoginForm, RegistrationForm, ProductForm
from app import app
from flask_login import current_user, login_user,logout_user, login_required

from app.models import User,Product,Cart,Order
from app import db
from config import Config



@app.route('/')
@app.route('/home')
def index():

    form = LoginForm()
    products = Product.query.all()[:6]
    try:
        user = User.query.get(session['user_id'])
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        return render_template('index.html', title='La Angel Collections| Home', form=form, products=products, cart_count=len(carts), user=user)
    except KeyError:
        form = LoginForm()
        return render_template('index.html', title='La Angel Collections| Home', form=form, products=products)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', "alert alert-danger")
            return redirect(url_for('login'))

        if user.email =='a@gmail.com':
            session['admin'] = True
            session['user_id'] = user.id

            login_user(user, remember=form.remember_me.data)
        session['user_id'] = user.id

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='La Angel Collections| Login', form=form)


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
        return redirect(url_for('login'))
    return render_template('signup.html', title='La Angel Collections| Signup', form=form)


@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if session['admin'] == True :
        products = Product.query.all()
        orders = Order.query.all()
        form = ProductForm()
        if request.method == 'POST':
            if request.files['image']:
                f = request.files['image']
                filename = secure_filename(f.filename)
                image_file = "static/images/products/"+ filename
                f.save(Config.UPLOAD_FOLDER + filename)
                product = Product(title=form.title.data,price=form.price.data, description=form.description.data,size=form.size.data,category=form.category.data,image=image_file)
                db.session.add(product)
                db.session.commit()
                flash('Congratulations')
                return redirect(url_for('dashboard'))
            product = Product(title=form.title.data, price=form.price.data, description=form.description.data,size=form.size.data, category=form.category.data)
            db.session.add(product)
            db.session.commit()
            flash('Congratulations')
            return redirect(url_for('dashboard'))
        else:
            user = User.query.get(session['user_id'])
            return render_template('dashboard.html', form=form, products=products, orders=orders, user=user,title='La Angel Collections| Dashboard',)
    else:
        return render_template('index.html',title='La Angel Collections| Home',)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    try:
        product = Product.query.get(product_id)
        form = LoginForm()
        user = User.query.get(session['user_id'])
        return render_template('product_detail.html', product=product, form=form, user=user,title='La Angel Collections| {}'.format(product.title))
    except:
        product = Product.query.get(product_id)
        form = LoginForm()
        return render_template('product_detail.html', product=product, form=form, title='La Angel Collections| {}'.format(product.title))


@app.route('/add/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    cart = Cart(product_id=product_id, user_id=session['user_id'], title=product.title, price=product.price,image=product.image)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:product_id>')
@login_required
def delete(product_id):
    try:
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('dashboard'))
    except:
        return render_template('dashboard.html', user=session['user_id'],title='La Angel Collections| Dashboard')



@app.route('/shopping-cart')
def shopping_cart():
    try:
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        total = 0
        for cart in carts:
            total += cart.price

        user = User.query.get(session['user_id'])
        return render_template('shopping_cart.html', title='La Angel Collections|Shopping cart ', cart_count=len(carts),carts=carts, total=total, user=user,)
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

        return redirect(url_for('order'))
    except KeyError:
        return redirect(url_for('index'))



@app.route('/order')
@login_required
def order():
    try:
        order = Order.query.filter_by(user_id=session['user_id']).first()
        carts = Cart.query.filter_by(user_id=session['user_id']).all()
        order_carts = carts.copy()
        print(order.amount)
        user = User.query.get(session['user_id'])
        db.session.add(order)
        db.session.commit()
        count = 0
        total = 0
        while count < len(carts):
            total += carts[count].price
            db.session.delete(carts[count])
            db.session.commit()
            count += 1
        return render_template('order.html', order=order, carts=order_carts, user=user, total=total,title='La Angel Collections | Order')
    except KeyError:
        return redirect(url_for('index'))

@app.route('/account/<username>')
@login_required
def account(username):
    try:
        user = User.query.filter_by(username=username).first()
        return render_template('account.html', user=user,title='La Angel Collections| {}'.format(user.username))
    except:
        return render_template('index.html',title='La Angel Collections| Home')



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