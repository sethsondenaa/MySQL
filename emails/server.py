from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'emails_dojo')
app.secret_key = "jkhasdiahoipnenaidoasdnfuhgqoerrssresyutei"


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/success/<entry>')
def success(entry):
	query = "SELECT email, DATE_FORMAT(created_at, '%m/%d/%y %H:%i %p') as date_entered FROM emails"
	emails = mysql.query_db(query)
	return render_template('success.html', all_emails=emails, entry=entry)

@app.route('/validate', methods=['POST'])
def validate():
	entry = request.form['email']
	query = "SELECT * FROM emails WHERE email = :email"
	data = {'email': entry}
	emails = mysql.query_db(query, data)
	if len(emails) > 0:
		return redirect('/success/' + entry) # If the query returns a result, redirect to success
	else:                           # If the query returns nothing, validation failed
		flash("Email is not valid!")
		return redirect('/')

@app.route('/delete/<delete_email>', methods=['POST'])
def delete(delete_email):
	query = "DELETE FROM emails WHERE email = :email"
	data = {'email': delete_email}
	mysql.query_db(query, data)
	return redirect('/success/email_deleted')

app.run(debug=True)