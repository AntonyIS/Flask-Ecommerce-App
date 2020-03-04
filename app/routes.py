from flask import render_template, url_for, flash, redirect,session
from app.forms import LoginForm, RegistrationForm
from app import app
from flask_login import current_user, login_user,logout_user

from app.models import User
from app import db



@app.route('/')
@app.route('/home')
def index():

    form = LoginForm()
    return render_template('index.html', title='Home page', form=form)


@app.route('/mali/<int:mali_id>')
def product_detail(mali_id):
    form = LoginForm()
    return render_template('product_detail.html', title='Home page', form = form)


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

        if user.email =='den@gmail.com':
            session['admin'] = True
            login_user(user, remember=form.remember_me.data)
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

@app.route('/dashboard')
def dashboard():
    if session['admin'] == True:

        return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('feedback.html', error=error, title='Antony Injila | 404'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('feedback.html', error=error), 500