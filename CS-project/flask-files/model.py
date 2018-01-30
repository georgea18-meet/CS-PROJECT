from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://george:george@localhost/cs_project'
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Account(UserMixin, db.Model):
	__tablename__ = 'account'
	id = db.Column('id', db.Integer, primary_key=True)
	
class Info(db.Model):
	__tablename__ = 'info'
	id = db.Column('id', db.Integer, primary_key=True)
	account = db.Column('account', db.Integer) 
	first_name = db.Column('first_name', db.Unicode)
	last_name = db.Column('last_name', db.Unicode)
	user_name = db.Column('user_name', db.Unicode, unique=True)
	password = db.Column('password', db.Unicode)
	profile_pic = db.Column('profile_pic',db.Unicode)
	BG_color = db.Column('BG_color', db.Unicode)
	main_color = db.Column('main_color', db.Unicode)
	groups = db.Column('groups', db.Unicode)
	friends = db.Column('friends', db.Unicode)
	friend_requests = db.Column('friend_requests', db.Unicode)

class Task(db.Model):
	__tablename__ = 'task'
	id = db.Column('id', db.Integer, primary_key=True)
	account = db.Column('account', db.Integer)
	task_title = db.Column('task_title', db.Unicode)
	task_text = db.Column('task_text', db.Unicode)
	deadline_d = db.Column('deadline_d', db.Integer)
	deadline_m = db.Column('deadline_m', db.Integer)
	deadline_y = db.Column('deadline_y', db.Integer)
	importance = db.Column('importance', db.Integer)
	time_needed = db.Column('time_needed', db.Integer)
	done = db.Column('done', db.Integer)

class Stage(db.Model):
	__tablename__ = 'stage'
	id = db.Column('id', db.Integer, primary_key=True)
	task = db.Column('task', db.Integer)
	account = db.Column('account', db.Integer)
	stage = db.Column('stage', db.Unicode)
	percent = db.Column('percent', db.Integer)
	done = db.Column('done', db.Integer)

class Group(db.Model):
	__tablename__ = 'group'
	id = db.Column('id', db.Integer, primary_key=True)
	name = db.Column('name', db.Unicode)
	members = db.Column('members', db.Unicode)
	profile_pic = db.Column('profile_pic',db.Unicode)

class Grouptask(db.Model):
	__tablename__ = 'grouptask'
	id = db.Column('id', db.Integer, primary_key=True)
	group = db.Column('group', db.Integer)
	created_by = db.Column('account', db.Integer)
	task_title = db.Column('task_title', db.Unicode)
	task_text = db.Column('task_text', db.Unicode)
	deadline_d = db.Column('deadline_d', db.Integer)
	deadline_m = db.Column('deadline_m', db.Integer)
	deadline_y = db.Column('deadline_y', db.Integer)
	importance = db.Column('importance', db.Integer)
	time_needed = db.Column('time_needed', db.Integer)
	done = db.Column('done', db.Integer)

class Comment(db.Model):
	__tablename__ = 'comment'
	id = db.Column('id', db.Integer, primary_key=True)
	comm_type = db.Column('type', db.Integer)
	task = db.Column('task', db.Integer)
	account = db.Column('account', db.Integer)
	text = db.Column('text', db.Unicode)

class Note(db.Model):
	__tablename__ = 'note'
	id = db.Column('id', db.Integer, primary_key=True)
	account = db.Column('account', db.Integer)
	group = db.Column('group', db.Integer)
	text = db.Column('text', db.Unicode)
	date = db.Column('date', db.Unicode)

class Update(db.Model):
	__tablename__ = 'update'
	id = db.Column('id', db.Integer, primary_key=True)
	noti_type = db.Column('type', db.Integer)
	account = db.Column('account', db.Integer)
	from_u = db.Column('from', db.Integer)
	text = db.Column('text', db.Unicode)
	date = db.Column('date', db.Unicode)
	par = db.Column('par', db.Integer)
	seen = db.Column('seen', db.Integer)

class Message(db.Model):
	__tablename__ = 'message'
	id = db.Column('id', db.Integer, primary_key=True)
	from_u = db.Column('from', db.Integer)
	to = db.Column('to', db.Integer)
	time = db.Column('time', db.Unicode)
	text = db.Column('text', db.Unicode)

db.create_all()