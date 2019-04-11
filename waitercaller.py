from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user
from flask import Flask
from flask import render_template
from flask import request
import json
import datetime
import dateparser
import string 
import config
from user import User
from mockdbhelper import MockDBHelper as DBHelper
from flask import redirect
from flask import url_for
from passwordhelper import PasswordHelper
import config
from bitlyhelper import BitlyHelper
from forms import RegistrationForm
from forms import LoginForm

app = Flask(__name__)
login_manager = LoginManager(app)
DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM' 

@app.route("/") 
def home():   
	registrationform = RegistrationForm()
	return render_template("home.html", registrationform=registrationform)

@app.route("/account")
@login_required
def account():
	tables = DB.get_tables(current_user.get_id())
	print(tables)
	return render_template("account.html", tables=tables)

@app.route("/login",methods = ['POST'])
def login():
	form = LoginForm(request.form)
	if form.validate():
		stored_user = DB.get_user(email)
		if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
			user = User(form.loginemail.data)
			#a cookie is given to the user here
			#keeping remembers true keeps the session active even after closing the browser
			login_user(user, remember=True)
			return redirect(url_for('account'))
		form.loginemail.errors.append("Email or password Invalid")
	return render_template("home.html", loginform=form, registrationform=RegistrationForm())


@app.route("/register", methods=["POST"])
def register():
	form = RegistrationForm(request.form)
	print(form.errors)
	if form.validate():
		print("holaaaaaaaaaaaaaaa")
		if(DB.get_user(form.email.data)):
			form.email.errors.append("Email address already registered")
			return render_template("home.html", registrationform=form)
		salt = str(PH.get_salt())
		hashed = PH.get_hash(form.password2.data+salt)   
		DB.add_user(form.email.data, salt, hashed)
		print("accepted")
		return render_template("home.html", registrationform=form, onloadmessage="Registration successful.Please log in.")
	print("rejected")
	return render_template("home.html", registrationform=form)

#session management
@login_manager.user_loader
def load_user(user_id):
	user_password = DB.get_user(user_id)
	if(user_password):
		return User(user_id)

@app.route("/logout") 
def logout():   
	logout_user()   
	return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
	now = datetime.datetime.now()
	requests = DB.get_request(current_user.get_id())
	#adding the waiting time in the queue
	for req in requests:
		deltaseconds = (now - req['time']).seconds
		req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds%60).zfill(2))
	return render_template("dashboard.html", requests=requests)

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
	request_id = request.args.get("request_id")
	DB.delete_request(request_id)
	return redirect(url_for('dashboard'))

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
	tablename = request.form.get("tablenumber")
	tableid = DB.add_table(tablename, current_user.get_id())
	new_url = BH.shorten_url(config.base_url + "newrequest/" +tableid)
	print(new_url)
	DB.update_table(tableid, new_url)
	return redirect(url_for('account'))

@app.route("/account/deletetable", methods=["POST","GET"])
@login_required
def account_deletetable():
	tableid = request.args.get("tableid")
	DB.delete_table(tableid)
	return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def new_request(tid):
	DB.add_request(tid)
	return "Your request has been logged and a waiter will be with you shortly"


if __name__ == '__main__':    
	app.run(port=5000, debug=True) 