from flask import Flask, render_template, redirect, request, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = "54adsfa5s6d4g684r6t4ty6ty4it6u4t6jhyk4j6sa5dgf46h8uo4po6asdfg1g"
mysql = MySQLConnector(app, 'usersdb')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def home():
	return redirect('/users')

@app.route('/users')
def index():
	query = "SELECT id, first_name, last_name, email, DATE_FORMAT(created_at, '%b %d, %Y') as created FROM users"
	user_list = mysql.query_db(query)
	return render_template('index.html', all_users=user_list)

@app.route('/users/new')
def add_user():
	return render_template('new_user.html')

@app.route('/users/<user_id>/edit')
def edit(user_id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {'id': user_id}
	user = mysql.query_db(query, data)
	return render_template('update.html', show_user=user)

@app.route('/update/<user_id>', methods=["POST"])
def update(user_id):
	errors = []
	form = request.form
	first_name = form["first_name"]
	last_name = form["last_name"]
	email = form["email"]
	#Check for errors
	if len(first_name) == 0:
		errors.append("Must enter a first name")
	if len(last_name) == 0:
		errors.append("Must enter a last name")
	if len(email) == 0:
		errors.append("Must enter an email")
	elif not EMAIL_REGEX.match(email):
		errors.append("Please enter a valid email address")
	if len(errors) == 0:
		#Update User	
		update_query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
		update_data = {
			'id': user_id,
			'first_name': request.form["first_name"],
			'last_name': request.form["last_name"],
			'email': request.form["email"],
		}
		mysql.query_db(update_query, update_data)
		return redirect('users/' + user_id)
	else:
		#Display Errors
		for error in errors:
			flash(error, "Add_Error")
		return redirect('/users/' + user_id + '/edit')

@app.route('/users/<user_id>')
def show(user_id):
	query = "SELECT * FROM users WHERE id = :id"
	data = {'id': user_id}
	user = mysql.query_db(query, data)
	return render_template('/user.html', show_user=user)

@app.route('/create', methods=["POST"])
def create():
	errors = []
	form = request.form
	first_name = form["first_name"]
	last_name = form["last_name"]
	email = form["email"]
	#Check for errors
	if len(first_name) == 0:
		errors.append("Must enter a first name")
	if len(last_name) == 0:
		errors.append("Must enter a last name")
	if len(email) == 0:
		errors.append("Must enter an email")
	elif not EMAIL_REGEX.match(email):
		errors.append("Please enter a valid email address")
	#If no errors
	if len(errors) == 0:
		#Create User
		query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
		data = {
			'first_name': first_name,
			'last_name': last_name,
			'email': email
		}
		mysql.query_db(query, data)
		return redirect('/users')
	#If errors
	else:
		#Display Errors
		for error in errors:
			flash(error, "Add_Error")
		return redirect('/users/new')

@app.route('/delete/<user_id>')
def destroy(user_id):
	query = "DELETE FROM users WHERE id = :id"
	data = {'id': user_id}
	mysql.query_db(query, data)
	return redirect('/users')

app.run(debug=True)