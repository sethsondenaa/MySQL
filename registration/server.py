from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re, md5
app = Flask(__name__)
mysql = MySQLConnector(app, 'registrationdb')
app.secret_key = "apsdipmvnkjnfpieorjulasdfncvajnsdfu498"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	query = "SELECT * FROM users"
	users = mysql.query_db(query)
	for user in users:
		if user['email'] == request.form['email']:
			if user['hashed_pw'] == md5.new(request.form['password']).hexdigest():
				return redirect('/success')
			else:
				flash("Incorrect password", "password_error")
				return redirect('/')
	flash("Email not found.", "email_error")
	return redirect('/')

@app.route('/process', methods=['POST'])
def process():
	if len(request.form["first_name"]) < 1 or len(request.form["last_name"]) < 1 or len(request.form["email"]) < 1 or len(request.form["password"]) < 1 or len(request.form["confirm_password"]) < 1:
		flash("Please enter all information.", "incomplete")
		return redirect('/')
	elif len(request.form["first_name"]) < 2:                                              
		flash("First name must be at least two characaters. Please re-enter a valid first name.", "first_name_error")
		return redirect('/')
	elif len(request.form["last_name"]) < 2:                                              
		flash("Last name must be at least two characters. Please re-enter a valid Last name.", "last_name_error")
		return redirect('/')
	elif not EMAIL_REGEX.match(request.form["email"]):
		flash("Please enter a valid email address.", "email_error")
		return redirect('/')
	elif not len(request.form["password"]) > 7:
		flash("Password must be at least 8 characters.", "password_error")
		return redirect('/')
	elif not request.form["password"] == request.form["confirm_password"]:
		flash("The passwords you entered did not match.", "password_error_two")
		return redirect('/')
	else:
		query = "INSERT INTO users (first_name, last_name, email, hashed_pw, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
		data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': md5.new(request.form['password']).hexdigest()
		}
		mysql.query_db(query, data)
		return redirect('/success')

@app.route('/success')
def success():
	return render_template('success.html')

app.run(debug=True)