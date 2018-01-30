from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://george:george@localhost/info_test'
db = SQLAlchemy(app)

class Rand(db.Model):
	__tablename__ = 'rand'
	id = db.Column('id',db.Integer,primary_key=True)
	first_name = db.Column('first_name',db.Unicode)
	last_name = db.Column('last_name',db.Unicode)

db.create_all()