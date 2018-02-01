from flask import Flask, render_template, request, redirect, url_for
from model import app, db, Account, Task, Info, Stage, Group
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#import os
#from werkzeug.utils import secure_filename
import time
import math
#from flask import send_from_directory
#UPLOAD_FOLDER = '/home/student/Desktop/CS-project/flask-files/static'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SECRET_KEY'] = 'thisissecret'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
import psycopg2

terms = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT9uQdYEsZMJywLXkjKgxexDzXrGfogPqjpYD6XCWn2oLjOg4xE','http://www.stickpng.com/assets/images/586fc02f3817baaba563b3f6.png','http://www.babywinkz.com/wp-content/uploads/2014/03/British-Summer-Time-BabyWinkz.jpg','https://pbs.twimg.com/profile_images/906422146993475584/4vcOQlGg.jpg']
names = db.session.query(Info).all()
for name in names:
	l = terms[name.id%4]
	name.profile_pic = l
db.session.commit()