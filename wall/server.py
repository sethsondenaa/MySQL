from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import MySQLConnector
from flask.ext.bcrypt import Bcrypt
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, "walldb")
app.secret_key = "6352143aiksudnjanfgpjbsndfgsdf68sdg4sd5f4goiashdjf"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
	if "logged_id" in session:
		return redirect('/dashboard')
	return render_template('index.html')


@app.route('/users', methods=["POST"])
def users():
	errors = []
	form = request.form
	action = form["action"]

	if action == "register":
		first_name = form["first_name"]
		last_name = form["last_name"]
		email = form["email"]
		pw = form["password"]
		
		if len(first_name) == 0:
			errors.append("Must enter a first name")
		if len(last_name) == 0:
			errors.append("Must enter a last name")
		if len(email) == 0:
			errors.append("Must enter an email")
		elif not EMAIL_REGEX.match(form["email"]):
			errors.append("Please enter a valid email address")
		if len(pw) == 0:
			errors.append("Must enter a password")
		elif not pw == form["confirm_pw"]:
			errors.append("Confirm password does not match password")

		if len(errors) == 0:
			query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
			data = {
				'first_name': first_name,
				'last_name': last_name,
				'email': email,
				'password': bcrypt.generate_password_hash(pw)
			}
			user = mysql.query_db(query, data)
			session["logged_id"] = user
			return redirect('/dashboard')
		else:
			for message in errors:
				flash(message, "register_error")
			return redirect('/')
	elif action == "login":
		email = form["email"]
		pw = form["password"]
		
		if len(email) == 0:
			errors.append("Must enter an email")
		if len(pw) == 0:
			errors.append("Must enter a password")
		if len(errors) > 0:
			for message in errors:
				flash(message, "logon_error")
			return redirect('/')
		else:
			query = "SELECT * FROM users WHERE email = :given_email"
			data = {
				"given_email":email
			}
			user = mysql.query_db(query, data)
			if len(user) > 0:
				user = user[0]
				if bcrypt.check_password_hash(user["password"], pw): #(stored password, inputed password)
					session["logged_id"] = user["id"]
					return redirect('/dashboard')
				else:
					flash("Incorrect password. Please try again.", "logon_error")
					return redirect('/')
			else:
				flash("Incorrect email. Please try again", "logon_error")
				return redirect('/')

@app.route('/dashboard')
def dashboard():
	if "logged_id" not in session:
		return redirect('/')
	query = "SELECT * FROM users WHERE id = :logged_id"
	data = {
		"logged_id": session["logged_id"]
	}
	messages_query = "SELECT first_name, message, messages.id, messages.users_id, messages.created_at FROM messages JOIN users ON users_id = users.id ORDER BY messages.created_at DESC"
	logged_user = mysql.query_db(query, data)
	messages = mysql.query_db(messages_query)
	comments_query = "SELECT first_name, comment, comments.id, comments.messages_id, comments.created_at FROM comments JOIN messages ON messages_id = messages.id JOIN users on comments.users_id = users.id ORDER BY comments.created_at ASC"
	comments = mysql.query_db(comments_query)
	return render_template('wall.html', current_user=logged_user[0], all_messages=messages, all_comments=comments)

@app.route('/messages', methods=["POST"])
def messages():
	query = "INSERT INTO messages (message, users_id, created_at, updated_at) VALUES (:message, :users_id, NOW(), NOW());"
	data = {
		'message': request.form["content"],
		'users_id': session["logged_id"]
	}
	instered_id = mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/comment/<message_id>', methods=["POST"])
def comment(message_id):
	query = "INSERT INTO comments (comment, users_id, messages_id, created_at, updated_at) VALUES (:comment, :users_id, :messages_id, NOW(), NOW());"
	data = {
		'comment': request.form["content"],
		'users_id': session["logged_id"],
		'messages_id': message_id
	}
	instered_id = mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/delete/<message_id>')
def delete_message(message_id):
	query = "DELETE FROM messages WHERE id = :id;"
	data = {'id':message_id}
	mysql.query_db(query, data)
	return redirect('/dashboard')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

app.run(debug=True)




























































