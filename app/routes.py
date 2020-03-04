from app import app


@app.route('/')
@app.route('/home')
def index():
    return 'hello world'