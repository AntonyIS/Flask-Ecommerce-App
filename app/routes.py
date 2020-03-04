from flask import render_template, url_for
from app import app


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home page')


@app.route('/mali/<int:mali_id>')
def product_detail(mali_id):
    return render_template('product_detail.html', title='Home page')



@app.errorhandler(404)
def not_found(error):
    return render_template('feedback.html', error=error, title='Antony Injila | 404'),404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('feedback.html', error=error), 500