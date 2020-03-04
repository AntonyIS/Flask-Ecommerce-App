from app import app
from flask_session import Session
sess = Session()
if __name__ == '__main__':
    app.run(debug=True)
