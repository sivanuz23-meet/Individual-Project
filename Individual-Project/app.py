from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {

  "apiKey": "AIzaSyCuS-h0Gw4gFtQJAuaPw15pnN9nEn1ZvxU",

  "authDomain": "individual-project-a2091.firebaseapp.com",

  "projectId": "individual-project-a2091",

  "storageBucket": "individual-project-a2091.appspot.com",

  "messagingSenderId": "422798657909",

  "appId": "1:422798657909:web:fc4cac3e10d4e59a7a2b3c",

  "measurementId": "G-R71QNN6H3L", "databaseURL": "https://individual-project-a2091-default-rtdb.europe-west1.firebasedatabase.app/",

}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		user = {"email": email, "password": password, "username" : request.form['Username']}
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			db.child('Users').child(login_session['user']['localId']).set(user)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			print (error)
	return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			print (error)
	return render_template("signin.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


@app.route('/profile', methods=['GET', 'POST'])
def profiles():
	return render_template('profile.html')

@app.route('/programming', methods=['GET', 'POST'])
def programming():
	if request.method == 'POST':
		user = db.child("Users").child(login_session['user']['localId']).get().val()
		username=user['username']
		message = {"msg" : request.form['msg'], "uid": login_session['user']['localId'], "username": username  }
		db.child('Messages').push(message)
		return render_template('programming.html', message = db.child('Messages').get().val())
	return render_template('programming.html')
@app.route("/signout")
def signout():
	login_session['user'] = None
	auth.current_user = None
	return redirect(url_for('signin'))
if __name__ == '__main__':
	app.run(debug=True)