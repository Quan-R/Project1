from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'passphrase'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://lnafruqnxnkkkt:5d956ce61c35bdfba0ba1f5a9f3beb8614be37890a87bec760a6a1611811f764@ec2-54-197-34-207.compute-1.amazonaws.com:5432/d5ermae68d7m6q"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

UPLOAD_FOLDER = './app/static/uploads'
db = SQLAlchemy(app)


app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import views

