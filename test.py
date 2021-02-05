from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#david - ive commented out my uri for security purposes
app.config['SQLALCHEMY_DATABASE_URI']='INSERT YOUR uri HERE'
db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postedby= db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    post = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
