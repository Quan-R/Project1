from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'passphrase'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qlkxdtuqzgjbdm:caeec71e30680830ea7c5b72ee58f00c9b39dedd39d1f54b8483e2db8bc8c3c6@ec2-3-211-48-92.compute-1.amazonaws.com:5432/d5v5g1eu8b09mr"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

UPLOAD_FOLDER = './app/static/uploads'
db = SQLAlchemy(app)


app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import views

