from flask import render_template, url_for
from app import app


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', title='Home page')