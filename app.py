from flask import Flask, render_template, request, redirect, url_for
#from model import Account, Task, Info, Stage, Group, Grouptask, Update, Comment, Note, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
#import os
#from werkzeug.utils import secure_filename
import time
import math
import psycopg2

#from flask import send_from_directory

#UPLOAD_FOLDER = '/home/student/Desktop/CS-project/flask-files/static'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://khwgribrjrkrfc:5742a9e8e262b6c2e740c7e83a685242f4fa3b665a02f22c82664d691dce14b1@ec2-54-83-203-198.compute-1.amazonaws.com:5432/d9fodf06bjket4'
app.config['SECRET_KEY'] = 'thisissecret'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

#models

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




def now():
	if (time.gmtime(time.time())[2]%10 == 1) and (time.gmtime(time.time())[2]!=11):
		return(time.strftime('%B %dst, %Y',time.gmtime(time.time())))
	elif (time.gmtime(time.time())[2]%10 == 2) and (time.gmtime(time.time())[2]!=12):
		return(time.strftime('%B %dnd, %Y',time.gmtime(time.time())))
	elif (time.gmtime(time.time())[2]%10 == 3) and (time.gmtime(time.time())[2]!=13):
		return(time.strftime('%B %drd, %Y',time.gmtime(time.time())))
	else:
		return(time.strftime('%B %dth, %Y',time.gmtime(time.time())))

'''def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS'''
@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

@app.route('/about')
def intro():
	return render_template('intro.html')

@app.route('/', methods=['GET','POST'])
def signin():
	if current_user.is_anonymous == False:
		return redirect(url_for('feed'))
	else:
		if request.method == 'GET':
			return render_template('login.html')
		else:
			user_name = request.form.get("user_name")
			password = request.form.get("password")
			user = db.session.query(Info).filter_by(user_name=user_name).first()
			all_accounts = db.session.query(Info).all()
			non = db.session.query(Info).filter_by(id=(all_accounts[len(all_accounts)-1].id+10)).first()
			if type(user) != type(non):
				if user.password == password:
					log = db.session.query(Account).filter_by(id=user.account).first()
					login_user(log)
					return redirect(url_for('feed'))
				else:
					return render_template('login.html')
			else:
				return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
	b = 0
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		users = db.session.query(Info).all()
		for i in users:
			if ((len(i.user_name)==0 or i.user_name.startswith(" "))) or ((len(i.password)==0 or i.password.startswith(" "))) or i.user_name == request.form.get("user_name"):
				b = 1
		if b == 0:
			log = Account()
			db.session.add(log)
			db.session.commit()
			user = Info()
			user.account = log.id
			user.first_name = request.form.get("first_name").capitalize()
			user.last_name = request.form.get("last_name").capitalize()
			user.user_name = request.form.get("user_name")
			user.password = request.form.get("password")
			user.profile_pic = "http://www.uva-aias.net/placeholders/avatar-male.png"
			user.BG_color = "#06AED5"
			user.main_color = "#086788"
			user.groups = "None"
			user.friends = "None"
			user.friend_requests = "None"
			db.session.add(user)
			db.session.commit()
			msg = Message()
			msg.from_u = 0
			msg.to = user.id
			msg.text = "Welcome to Tasky!\r We are glad that you decided to join our motivating and productive environment. Here you can manage your own tasks, as well as your group and individual projects. If you have any questions, reply to this message, and we'll be more than happy to answer any of them.\r Let it be the reason of your success.\r \r Tasky."
			msg.time = time.strftime('%d/%m/%Y %H:%M:%S',time.gmtime(time.time()))
			db.session.add(msg)
			db.session.commit()
			noti = Update()
			noti.noti_type = 5
			noti.account = msg.to
			noti.from_u = msg.from_u
			noti.text = user.first_name+" "+user.last_name+" has sent you a message '"+msg.text+".'"
			noti.date = now()
			noti.par = msg.id
			noti.seen = 0
			db.session.add(noti)
			db.session.commit()
			return redirect(url_for("signin"))
		else:
			return render_template('signup.html')

@app.route('/tasks/main/<int:sort>/<int:filtered>')
@login_required
def main(sort=0,filtered=1):
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	all_tasks = db.session.query(Task).filter_by(account=user.account).all()
	if filtered==1:
		tasks = [];
		for t in all_tasks:
			if t.done == 0:
				tasks.append(t)
	elif filtered==2:
		tasks = [];
		for t in all_tasks:
			if t.done == 1:
				tasks.append(t)
	else:
		tasks = all_tasks
	expired=[]
	for t in tasks:
		if time.mktime((t.deadline_y,t.deadline_m,t.deadline_d,0,0,0,0,0,0))<time.time():
			expired.append(t.id)
	if sort == 0:
		tasks.reverse()
	elif sort == 1:
		sorted_tasks = []
		for t in tasks:
			sorted_tasks.append((time.mktime((t.deadline_y,t.deadline_m,t.deadline_d,0,0,0,0,0,0))-time.time(),t.id))
		sorted_tasks.sort()
		tasks = []
		for t in sorted_tasks:
			tasks.append(db.session.query(Task).filter_by(id=t[1]).first())
	elif sort == 2:
		sorted_tasks = []
		for t in tasks:
			sorted_tasks.append((t.importance,t.id))
		sorted_tasks.sort()
		tasks = []
		for t in sorted_tasks:
			tasks.append(db.session.query(Task).filter_by(id=t[1]).first())
		tasks.reverse()
	elif sort == 3:
		sorted_tasks = []
		for t in tasks:
			sorted_tasks.append((t.time_needed,t.id))
		sorted_tasks.sort()
		tasks = []
		for t in sorted_tasks:
			tasks.append(db.session.query(Task).filter_by(id=t[1]).first())
		'''elif sort == 4:
			sorted_tasks = []
			for t in tasks:
				rank = t.importance-(t.time_needed)*2-4*math.log10(time.mktime((t.deadline_y,t.deadline_m,t.deadline_d,0,0,0,0,0,0))-time.time())
				sorted_tasks.append((rank,t.id))
			sorted_tasks.sort()
			tasks = []
			for t in sorted_tasks:
				tasks.append(db.session.query(Task).filter_by(id=t[1]).first())
			tasks.reverse()'''
	deadlines = []
	for task in tasks:
		deadlines.append(time.mktime((task.deadline_y,task.deadline_m,task.deadline_d,0,0,0,0,0,0)))
	return render_template('main.html',user=user,tasks=tasks,len=len(tasks),deadlines=deadlines,current_time=time.time(),sort=sort,filtered=filtered)

@app.route('/main')
@login_required
def feed():
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	notis = db.session.query(Update).filter_by(account=user.id).all()
	notifications = []
	for n in notis:
		u = db.session.query(Info).filter_by(id=int(n.from_u)).first()
		notifications.append((n,u,n.seen,n.id))
		n.seen = 1
	notifications.sort(key= lambda noti:noti[3])
	notifications.reverse()
	db.session.commit()
	return render_template('feed.html',notifications=notifications,user=user)


@app.route('/add',methods=['GET','POST'])
@login_required
def add_task():
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	if request.method == 'GET':
		return render_template('add_task.html',user=user)
	else:
		task = Task()
		task.account = user.account
		task.task_title = request.form.get('task_title')
		task.task_text = request.form.get('task_text')
		deadline = time.strptime(request.form.get('deadline'), "%Y-%m-%d")
		task.deadline_d = deadline[2]
		task.deadline_m = deadline[1]
		task.deadline_y = deadline[0]
		task.importance = request.form.get('importance')
		task.time_needed = request.form.get('time_needed')
		task.done = 0
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('main',sort=0,filtered=1))

@app.route('/group/<int:group_id>/add/task',methods=['GET','POST'])
@login_required
def add_grouptask(group_id):
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	if request.method == 'GET':
		return render_template('add_grouptask.html',user=user,group_id=group_id)
	else:
		task = Grouptask()
		task.group = group_id
		task.created_by = user.account
		task.task_title = request.form.get('task_title')
		task.task_text = request.form.get('task_text')
		deadline = time.strptime(request.form.get('deadline'), "%Y-%m-%d")
		task.deadline_d = deadline[2]
		task.deadline_m = deadline[1]
		task.deadline_y = deadline[0]
		task.importance = request.form.get('importance')
		task.time_needed = request.form.get('time_needed')
		task.done = 0
		db.session.add(task)
		group = db.session.query(Group).filter_by(id=group_id).first()
		mems = group.members.split(" ")
		for i in mems:
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 3
				noti.account = i
				noti.from_u = str(user.id)
				noti.text = user.first_name+" "+user.last_name+" has added the task '"+task.task_title+"' to the project '"+group.name+".'"
				noti.date = time.strftime("%d/%m/%Y",time.gmtime(time.time()))
				noti.par = task.id
				noti.seen = 0
				db.session.add(noti)
		db.session.commit()
		return redirect(url_for('group',group_id=group_id))


@app.route('/task/<int:task_id>',methods=['GET','POST'])
@login_required
def task(task_id):
	if request.method == 'GET':
		task = db.session.query(Task).filter_by(id=task_id).first()
		log = db.session.query(Account).filter_by(id=task.account).first()
		if log == current_user:
			user = db.session.query(Info).filter_by(account=task.account).first()
			days = (time.mktime((task.deadline_y,task.deadline_m,task.deadline_d,0,0,0,0,0,0))-time.time())/(24*3600)
			if math.ceil(days)-days>=0.5:
				days = int(math.ceil(days))
			else:
				days = int(math.floor(days))
			return render_template('task.html',task=task, days=days, user=user)
		else:
			logout_user()
			return redirect(url_for('signin'))
	else:
		task = db.session.query(Task).filter_by(id=task_id).first()
		task.done = 1
		db.session.commit()
		return redirect(url_for('main',sort=0,filtered=1))

@app.route('/group/task/<int:task_id>',methods=['GET','POST'])
@login_required
def grouptask(task_id):
	user = db.session.query(Info).filter_by(id=current_user.id).first()
	if request.method == 'GET':
		task = db.session.query(Grouptask).filter_by(id=task_id).first()
		comms = db.session.query(Comment).filter_by(comm_type=1,task=task.id).all()
		comments = []
		for c in comms:
			u = db.session.query(Info).filter_by(account=c.account).first()
			comments.append((c,u))
		days = (time.mktime((task.deadline_y,task.deadline_m,task.deadline_d,0,0,0,0,0,0))-time.time())/(24*3600)
		if math.ceil(days)-days>=0.5:
			days = int(math.ceil(days))
		else:
			days = int(math.floor(days))
		return render_template('grouptask.html',task=task,days=days,user=user,comments=comments)
	else:
		task = db.session.query(Grouptask).filter_by(id=task_id).first()
		group = db.session.query(Group).filter_by(id=task.group).first()
		task.done = 1
		notis_d = db.session.query(Update).filter_by(noti_type=3,par=str(task.id)).all()
		for no in notis_d:
			db.session.delete(no)
		mems = group.members.split(" ")
		for i in mems:
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 2
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has marked the task '"+task.task_title+"' in the project '"+group.name+"' as done."
				noti.date = now()
				noti.par = group.id
				noti.seen = 0
				db.session.add(noti)
		db.session.commit()
		return redirect(url_for('group',group_id=task.group))

@app.route('/group/task/<int:task_id>/comment',methods=['GET','POST'])
@login_required
def add_comment(task_id):
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	task = db.session.query(Grouptask).filter_by(id=task_id).first()
	group = db.session.query(Group).filter_by(id=task.group).first()
	if request.method !='GET':
		comment = Comment()
		comment.comm_type = 1
		comment.task = task_id
		comment.account = user.id
		comment.text = request.form.get("comment")
		db.session.add(comment)
		for i in group.members.split(" "):
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 3
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has commented on the task '"+task.task_title+": '"+comment.text+".'"
				noti.date = now()
				noti.par = task_id
				noti.seen = 0
				db.session.add(noti)
		db.session.commit()
	return redirect(url_for('grouptask',task_id=task_id))

@app.route('/group/note/<int:note_id>/comment',methods=['GET','POST'])
@login_required
def add_comment_note(note_id):
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	task = db.session.query(Note).filter_by(id=note_id).first()
	group = db.session.query(Group).filter_by(id=task.group).first()
	if request.method !='GET':
		comment = Comment()
		comment.comm_type = 2
		comment.task = note_id
		comment.account = user.id
		comment.text = request.form.get("comment")
		db.session.add(comment)
		for i in group.members.split(" "):
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 4
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has commented on the note '"+task.text+"': '"+comment.text+".'"
				noti.date = now()
				noti.par = note_id
				noti.seen = 0
				db.session.add(noti)
		db.session.commit()
	return redirect(url_for('note',note_id=note_id))	

@app.route('/group/task/comment/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
	comment = db.session.query(Comment).filter_by(id=comment_id).first()
	task_id = comment.task
	if current_user.id == comment.account:
		db.session.delete(comment)
		db.session.commit()
	return redirect(url_for('grouptask',task_id=task_id))

@app.route('/group/note/comment/<int:comment_id>/delete')
@login_required
def delete_comment_note(comment_id):
	comment = db.session.query(Comment).filter_by(id=comment_id).first()
	task_id = comment.task
	if current_user.id == comment.account:
		db.session.delete(comment)
		db.session.commit()
	return redirect(url_for('note',note_id=task_id))

@app.route('/profile/settings',methods=['GET','POST'])
@login_required
def profile_edit():
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	if request.method=='GET':
		return render_template('profile_settings.html',user=user)
	else:
		if request.form.get('old_password')==user.password:
			user.first_name = request.form.get("first_name").capitalize()
			user.last_name = request.form.get("last_name").capitalize()
			user.user_name = request.form.get("user_name")
			if request.form.get("password") != "":
				user.password = request.form.get("password")
			user.profile_pic = request.form.get("profile_pic")
			user.BG_color = request.form.get("BG_color")
			db.session.commit()
		return redirect(url_for('profile'))

@app.route('/task/<int:task_id>/edit',methods=['GET','POST'])
@login_required
def edit_task(task_id):
	task = db.session.query(Task).filter_by(id=task_id).first()
	log = db.session.query(Account).filter_by(id=task.account).first()
	if log == current_user:
		if request.method == 'GET':
			user = db.session.query(Info).filter_by(account=task.account).first()
			return render_template('edit_task.html',task=task,user=user)
		else:
			if request.form.get('task_title') != '':
				task.task_title = request.form.get('task_title')
			if request.form.get('task_text') != '':
				task.task_text = request.form.get('task_text')
			if request.form.get('deadline') != '':
				deadline = time.strptime(request.form.get('deadline'), "%Y-%m-%d")
				task.deadline_d = deadline[2]
				task.deadline_m = deadline[1]
				task.deadline_y = deadline[0]
			if request.form.get('importance') != '':
				task.importance = request.form.get('importance')
			if request.form.get('time_needed') != '':
				task.time_needed = request.form.get('time_needed')
			db.session.commit()
			return redirect(url_for('task',task_id=task.id))

@app.route('/group/task/<int:task_id>/edit',methods=['GET','POST'])
@login_required
def edit_grouptask(task_id):
	task = db.session.query(Grouptask).filter_by(id=task_id).first()
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	if request.method == 'GET':
		return render_template('edit_grouptask.html',task=task,user=user)
	else:
		if request.form.get('task_title') != '':
			task.task_title = request.form.get('task_title')
		if request.form.get('task_text') != '':
			task.task_text = request.form.get('task_text')
		if request.form.get('deadline') != '':
			deadline = time.strptime(request.form.get('deadline'), "%Y-%m-%d")
			task.deadline_d = deadline[2]
			task.deadline_m = deadline[1]
			task.deadline_y = deadline[0]
		if request.form.get('importance') != '':
			task.importance = request.form.get('importance')
		if request.form.get('time_needed') != '':
			task.time_needed = request.form.get('time_needed')
		group = db.session.query(Group).filter_by(id=task.group).first()
		mems = group.members.split(" ")
		for i in mems:
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 3
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has editted the task '"+task.task_title+"' in the project '"+group.name+".'"
				noti.date = now()
				noti.par = task.id
				noti.seen = 0
		db.session.commit()
		return redirect(url_for('grouptask',task_id=task.id))

@app.route('/main/profile')
@login_required
def profile():
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	tasks = db.session.query(Task).filter_by(account=user.id).all()
	done = 0
	for t in tasks:
		if t.done == 1:
			done=done+1
	month = time.gmtime(time.time())[1]
	ta_mon = db.session.query(Task).filter_by(deadline_m=month).all()
	monthly = 0
	for t in ta_mon:
		if t.account == user.id:
			if t.deadline_y == time.gmtime(time.time())[0]:
				monthly = monthly+1
	month = time.strftime("%B")
	requests = []
	if user.friend_requests != "None":
		reqs = user.friend_requests.split(" ")
		for r in reqs:
			req = db.session.query(Info).filter_by(id=int(r)).first()
			requests.append(req)
	len_req = len(requests)
	friends = []
	if user.friends != "None":
		reqs = user.friends.split(" ")
		for r in reqs:
			req = db.session.query(Info).filter_by(id=int(r)).first()
			friends.append(req)
	len_fri = len(friends)
	return render_template('profile_page.html',monthly=monthly,month=month,done=done,tasks=len(tasks),user=user,requests=requests,friends=friends,len_req=len_req,len_fri=len_fri)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('signin'))

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
	task = db.session.query(Task).filter_by(id=task_id).first()
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for('main',sort=0,filtered=1))

@app.route('/group/delete_task/<int:task_id>')
@login_required
def delete_grouptask(task_id):
	task = db.session.query(Grouptask).filter_by(id=task_id).first()
	group = db.session.query(Group).filter_by(id=task.group).first()
	user = db.session.query(Info).filter_by(id=current_user.id).first()
	notis_d = db.session.query(Update).filter_by(noti_type=3,par=str(task.id)).all()
	for no in notis_d:
		db.session.delete(no)
	mems = group.members.split(" ")
	for i in mems:
		if i != str(user.id):
			noti = Update()
			noti.noti_type = 2
			noti.account = i
			noti.from_u = user.id
			noti.text = user.first_name+" "+user.last_name+" has deleted the task '"+task.task_title+"' from the project '"+group.name+".'"
			noti.date = now()
			noti.par = group.i
			noti.seen = 0
			db.session.add(noti)
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for('group',group_id=group.id))

@app.route('/add_friends')
@login_required
def add_friends():
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	all_users = db.session.query(Info).all()
	users = []
	for u in all_users:
		if u.user_name != user.user_name:
			m = 0
			if user.friends == "None":
				is_friend = 0
			else:
				friends = str(user.friends).split(" ")
				is_friend = 0
				for r in friends:
					if r == str(u.id):
						is_friend = 1
			if is_friend == 0:
				for f in str(u.friends).split(" "):
					if (str(user.friends).split(" ").count(f) > 0 and f != "None"):
						m+=1
			users.append((u,is_friend,m))
	return render_template('add_friends.html',users=users, user=user)

@app.route('/profile/<int:user_id>',methods=['GET','POST'])
@login_required
def strange_profile(user_id):
	log = current_user
	u = db.session.query(Info).filter_by(account=log.id).first()
	user = db.session.query(Info).filter_by(id=user_id).first()
	if u == user:
		return redirect(url_for('profile'))
	else:
		tasks = db.session.query(Task).filter_by(account=user.account).all()
		done = 0
		for t in tasks:
			if t.done == 1:
				done=done+1
		month = time.gmtime(time.time())[1]
		ta_mon = db.session.query(Task).filter_by(deadline_m=month).all()
		monthly = 0
		for t in ta_mon:
			if t.account == user.id:
				if t.deadline_y == time.gmtime(time.time())[0]:
					monthly = monthly+1
		month = time.strftime("%B")

		if user.friends == "None":
			is_friend = 0
		else:
			friends = str(user.friends).split(" ")
			is_friend = 0
			for r in friends:
				if r == str(u.id):
					is_req = 0
					am_req = 0
					is_friend = 1


		requests = str(user.friend_requests).split(" ")	
		
		if is_friend == 0:
			if user.friend_requests != "None":
				requests = str(user.friend_requests).split(" ")
				is_req = 0
				for r in requests:
					if int(r) == u.id:
						is_req = 1
			else:
				is_req = 0
			am_req = 0
			if is_req == 0:
				if u.friend_requests == "None":
					am_req = 0
				else:
					reqs = u.friend_requests.split(" ")
					for r in reqs:
						if int(r) == user.id:
							am_req = 1

		if request.method == 'GET':
			return render_template('friend_profile.html',monthly=monthly,month=month,done=done,tasks=len(tasks),user=user,u=u, is_req=is_req, am_req=am_req, is_friend=is_friend)
		else:
			sub = request.form.get('add_button')
			if is_friend == 0:
				if (is_req == 0) and (am_req == 0):
					if user.friend_requests == "None":
						user.friend_requests = str(u.id)
					else:
						user.friend_requests = user.friend_requests+" "+str(u.id)
					is_req = 1
					noti = Update()
					noti.noti_type = 1
					noti.account = user.id
					noti.from_u = u.id
					noti.text = u.first_name+" "+u.last_name+" has sent you a friendship request."
					noti.date = now()
					noti.par = u.id
					noti.seen = 0
					db.session.add(noti)
				elif (is_req == 1) and (am_req == 0) :
					if user.friend_requests == requests[0]:
						user.friend_requests = "None"
					else:
						requests.remove(str(u.id))
						user.friend_requests = requests[0]
						for r in range(1,len(requests)-1):
							user.friend_requests = user.friend_requests+" "+requests[r]
					is_req = 0
					noti = db.session.query(Update).filter_by(noti_type=1, account=user.id, from_u=u.id).first()
					db.session.delete(noti)
				elif (is_req == 0) and (am_req==1):
					requests = str(u.friend_requests).split(" ")
					if u.friend_requests == requests[0]:
						u.friend_requests = "None"
					else:
						requests.remove(str(user.id))
						u.friend_requests = requests[0]
						for r in range(1,len(requests)):
							u.friend_requests = u.friend_requests+" "+requests[r]
					if u.friends == "None":
						u.friends = str(user.id)
					else:
						u.friends = u.friends+" "+str(user.id)
					if user.friends == "None":
						user.friends = str(u.id)
					else:
						user.friends = user.friends+" "+str(u.id)
					is_friend = 1
					noti_d = db.session.query(Update).filter_by(noti_type=1, account=u.id, from_u=user.id).first()
					noti = Update()
					noti.noti_type = 1
					noti.account = user.id
					noti.from_u = u.id
					noti.text = u.first_name+" "+u.last_name+" has accepted your friendship request."
					noti.date = now()
					noti.par = u.id
					noti.seen = 0
					db.session.delete(noti_d)
					db.session.add(noti)
			else:
				friends = str(u.friends).split(" ")
				if u.friends == friends[0]:
					u.friends = "None"
				else:
					friends.remove(str(user.id))
					u.friends = friends[0]
					for r in range(1,len(friends)):
						u.friends = u.friends+" "+friends[r]
				
				friends = str(user.friends).split(" ")
				if user.friends == friends[0]:
					user.friends = "None"
				else:
					friends.remove(str(u.id))
					user.friends = friends[0]
					for r in range(1,len(friends)):
						user.friends = user.friends+" "+friends[r]
				is_friend = 0

			db.session.commit()
			return render_template('friend_profile.html',monthly=monthly,month=month,done=done,tasks=len(tasks),user=user,u=u, is_req=is_req, am_req=am_req, is_friend=is_friend)
			
@app.route('/group/create',methods=['GET','POST'])
@login_required
def create_group():
	log = current_user
	user = db.session.query(Info).filter_by(id=log.id).first()
	friends = []
	if user.friends != "None":
		friends_id = str(user.friends).split(" ")
		for r in friends_id:
			friend = db.session.query(Info).filter_by(id=int(r)).first()
			friends.append(friend)
	if request.method == 'GET':
		return render_template('create_group.html',friends=friends, user=user)
	else:
		group = Group()
		group.name = request.form.get('name')
		members = request.form.getlist('member')
		group.members = str()
		for i in members:
			group.members = group.members+' '+str(i)
		group.members = str(user.id)+group.members
		group.tasks = "None"
		db.session.add(group)
		db.session.commit()
		members = group.members.split(" ")
		for i in members:
			member = db.session.query(Info).filter_by(id=int(i)).first()
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 2
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" created the project '"+group.name+".'"
				noti.date = time.strftime("%d/%m/%Y",time.gmtime(time.time()))
				noti.par = group.id
				noti.seen = 0
				db.session.add(noti)
			if member.groups == "None":
				member.groups = str(group.id)
			else:
				member.groups = member.groups+' '+str(group.id)
		group.profile_pic = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQph9xs7vDHjyHL7EyKLPmyPEyG0kC5QsrNLQEIdJ70RJQSPyzULw"
		db.session.commit()
		return redirect(url_for('group',group_id=group.id))

@app.route('/group/edit/<int:group_id>',methods=['GET','POST'])
@login_required
def edit_group(group_id):
	log = current_user
	user = db.session.query(Info).filter_by(id=log.id).first()
	group = db.session.query(Group).filter_by(id=group_id).first()
	members = group.members.split(" ")
	friends = []
	if user.friends != "None":
		friends_id = str(user.friends).split(" ")
		for r in friends_id:
			is_member = 0
			friend = db.session.query(Info).filter_by(id=int(r)).first()
			for m in members:
				if m == str(friend.id):
					is_member = 1
			friends.append((friend,is_member))
	if request.method == 'GET':
		return render_template('group_settings.html',friends=friends,user=user,group_id=group_id,group=group)
	else:
		group.name = request.form.get('name')
		members = request.form.getlist('member')
		for i in group.members.split(" "):
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 2
				noti.account = int(i)
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has editted the project '"+group.name+".'"
				noti.date = now()
				noti.par = group.id
				noti.seen = 0
				db.session.add(noti)
		for i in members:
			if group.members.split(" ").count(str(i)) == 0:
				u = db.session.query(Info).filter_by(id=int(i)).first()
				if i != user.id:
					noti = Update()
					noti.noti_type = 2
					noti.account = i
					noti.from_u = user.id
					noti.text = user.first_name+" "+user.last_name+" has added you to the project '"+group.name+".'"
					noti.date = now()
					noti.par = group.id
					noti.seen = 0
					db.session.add(noti)
				if u.groups == "None":
					u.groups = str(group.id)
				else:
					u.groups = u.groups+' '+str(group.id)
				for j in group.members.split(" "):
					if j != str(user.id):
						noti = Update()
						noti.noti_type = 2
						noti.account = j
						noti.from_u = user.id
						noti.text = user.first_name+" "+user.last_name+" has added "+u.first_name+" "+u.last_name+" to the project '"+group.name+".'"
						noti.date = now()
						noti.par = group.id
						noti.seen = 0
						db.session.add(noti)
		for i in group.members.split(" "):
			if members.count(i) == 0 and i != str(user.id):
				u = db.session.query(Info).filter_by(id=int(i)).first()
				if i != str(user.id):
					notis_d = db.session.query(Update).filter_by(noti_type=2,par=group.id,account=int(i)).all()
					for n in notis_d:
						db.session.delete(n)
					noti = Update()
					noti.noti_type = 1
					noti.account = int(i)
					noti.from_u = user.id
					noti.text = user.first_name+" "+user.last_name+" has removed you from the project '"+group.name+".'"
					noti.date = now()
					noti.par = user.id
					noti.seen = 0
					db.session.add(noti)
				if u.groups == str(group.id):
					u.groups = "None"
				else:
					l = u.groups.split(" ")
					u.groups = l[0]
					for m in range(1,len(l)):
						u.groups+=" "+l[m]
				for j in group.members.split(" "):
					if j != str(user.id) and j != str(u.id):
						noti = Update()
						noti.noti_type = 2
						noti.account = j
						noti.from_u = user.id
						noti.text = user.first_name+" "+user.last_name+" has removed "+u.first_name+" "+u.last_name+" from the project '"+group.name+".'"
						noti.date = now()
						noti.par = group.id
						noti.seen = 0
						db.session.add(noti)
		group.members = str()
		for i in members:
			group.members = group.members+' '+str(i)
		group.members = str(user.id)+group.members
		group.profile_pic = request.form.get('profile_pic')
		db.session.commit()
		return redirect(url_for('group',group_id=group_id))

@app.route('/group/<int:group_id>')
@login_required
def group(group_id):
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	group = db.session.query(Group).filter_by(id=group_id).first()
	tasks = db.session.query(Grouptask).filter_by(group=group_id).all()
	notes = db.session.query(Note).filter_by(group=group_id).all()
	deadlines = []
	accounts = []
	for task in tasks:
		deadlines.append(time.mktime((task.deadline_y,task.deadline_m,task.deadline_d,0,0,0,0,0,0)))
	tasks.reverse()
	deadlines.reverse()
	for note in notes:
		accounts.append(db.session.query(Info).filter_by(id=note.account).first())
	notes.reverse()
	accounts.reverse()
	members = group.members.split(" ")
	p = 0
	mems = []
	for m in members:
		mem = db.session.query(Info).filter_by(id=m).first()
		mems.append(mem)
		if m == str(user.id):
			p =1
	if p == 0:
		return redirect(url_for('logout'))
	else:
		return render_template('group.html',members=mems,user=user,group=group,tasks=tasks,deadlines=deadlines,len_t=len(tasks),len_n=len(notes),current_time=time.time(),accounts=accounts,notes=notes)

@app.route('/group/main')
@login_required
def my_groups():
	log = current_user
	user = db.session.query(Info).filter_by(id=log.id).first()
	all_groups = db.session.query(Group).all()
	groups = []
	if user.groups != "None":
		gros = user.groups.split(" ")
		if len(gros) != 0:
			for gro in gros:
				group = db.session.query(Group).filter_by(id=gro).first()
				members =[]
				if group.members!="None":
					for m in group.members.split(" "):
						member = db.session.query(Info).filter_by(id=m).first()
						members.append(member)
					groups.append((group,members))
					show = 1
				else:
					show = 0
		else:		
			show = 0
	else:
		show = 0
	return render_template('my_groups.html',user=user,groups=groups,show=show)

@app.route('/group/<int:group_id>/leave')
@login_required
def leave(group_id):

	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	group = db.session.query(Group).filter_by(id=group_id).first()
	members = group.members.split(" ")
	groups = user.groups.split(" ")
	members.remove(str(user.id))
	groups.remove(str(group.id))
	notis_d = db.session.query(Update).filter_by(noti_type=2,account=user.id,par=group.id).all()
	for no in notis_d:
		db.session.delete(no)
	if len(groups)>0:
		user.groups = groups[0]
		for r in range(1,len(groups)):
			user.groups = user.groups+" "+groups[r]
		if len(members)>0:
			group.members = members[0]
			for r in range(1,len(members)):
				group.members = group.members+" "+members[r]
			for i in group.members.split(" "):
				noti = Update()
				noti.noti_type = 2
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has left the project '"+group.name+".'"
				noti.date = now()
				noti.par = group.id
				noti.seen = 0
				db.session.add(noti)
		else:
			group.members = "None"
	else:
		user.groups = "None"
		group.members = "None"
	db.session.commit()
	return redirect(url_for('my_groups'))

@app.route('/group/<int:group_id>/add/note',methods=['GET','POST'])
def add_note(group_id):
	log = current_user
	user = db.session.query(Info).filter_by(account=log.id).first()
	group = db.session.query(Group).filter_by(id=group_id).first()
	if request.method == 'GET':
		return render_template('add_note.html',user=user,group_id=group_id)
	else:
		note = Note()
		note.account = user.id
		note.group = group_id
		#note.title = request.form.get('note_title')
		note.text = request.form.get('note_text')
		note.date = now()
		db.session.add(note)
		db.session.commit()
		for i in group.members.split(" "):
			if i != str(user.id):
				noti = Update()
				noti.noti_type = 4
				noti.account = i
				noti.from_u = user.id
				noti.text = user.first_name+" "+user.last_name+" has posted a new note to the group '"+group.name+"': '"+note.text+".'"
				noti.date = now()
				noti.par = note.id
				noti.seen = 0
				db.session.add(noti)
		db.session.commit()
		return redirect(url_for('note',note_id=note.id))

@app.route('/group/note/<int:note_id>')
@login_required
def note(note_id):
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	note = db.session.query(Note).filter_by(id=note_id).first()
	account = db.session.query(Info).filter_by(id=note.account).first()
	comms = db.session.query(Comment).filter_by(comm_type=2,task=note.id).all()
	comments = []
	for c in comms:
		u = db.session.query(Info).filter_by(account=c.account).first()
		comments.append((c,u))
	return render_template('note.html',user=user,note=note,account=account,comments=comments)

@app.route('/group/delete_note/<int:note_id>')
@login_required
def delete_note(note_id):
	note = db.session.query(Note).filter_by(id=note_id).first()
	notis = db.session.query(Update).filter_by(noti_type=4,par=note.id).all()
	g = note.group
	for n in notis:
		db.session.delete(n)
	db.session.delete(note)
	db.session.commit()
	return redirect(url_for('group',group_id=g))

@app.route('/send/<int:user_id>', methods=['GET','POST'])
@login_required
def send(user_id):
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	u = db.session.query(Info).filter_by(id=user_id).first()
	if request.method == 'GET':
		return render_template('write_message.html',user=user,u=u)
	else:
		msg = Message()
		msg.from_u = user.id
		msg.to = u.id
		msg.text = request.form.get('msg_text')
		msg.time = time.strftime('%d/%m/%Y %H:%M:%S',time.gmtime(time.time()))
		db.session.add(msg)
		db.session.commit()
		noti = Update()
		noti.noti_type = 5
		noti.account = msg.to
		noti.from_u = msg.from_u
		noti.text = user.first_name+" "+user.last_name+" has sent you a message '"+msg.text+".'"
		noti.date = now()
		noti.par = msg.id
		noti.seen = 0
		db.session.add(noti)
		db.session.commit()
		return redirect(url_for('inbox'))

@app.route('/profile/inbox/message/<int:msg_id>')
@login_required
def message(msg_id):
	msg = db.session.query(Message).filter_by(id=msg_id).first()
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	if msg.u_from == 0:
		u = db.session.query(Info).filter_by(user_name="tasky_2018").first()
	else:
		u = db.session.query(Info).filter_by(id=msg.from_u).first()
	return render_template('message.html',msg=msg,u=u,user=user)

@app.route('/profile/inbox')
@login_required
def inbox():
	user = db.session.query(Info).filter_by(account=current_user.id).first()
	all_messages = db.session.query(Message).filter_by(to=user.id).all()
	messages = []
	for m in all_messages:
		if msg.u_from == 0:
			u = db.session.query(Info).filter_by(user_name="tasky_2018").first()
		else:
			u = db.session.query(Info).filter_by(id=msg.from_u).first()
		messages.append((m,u,m.id))
	messages.sort(key = lambda n:n[2])
	messages.reverse()
	return render_template('inbox.html',messages=messages,user=user)

if __name__ == "__main__":
	app.run(debug=True)
