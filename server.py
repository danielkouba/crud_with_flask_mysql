from flask import Flask, request, render_template, redirect, session, flash
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql =  MySQLConnector(app, 'friends_db')

app.secret_key = "GoGoPowerRangersYouMightyMorphinPowerRangers"

@app.route('/')
def index():
	#list friends
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('index.html', all_friends = friends)

@app.route('/friends', methods=['POST'])
def create():
	#Handle the add friend form submit and create the friend in the DB
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES( :first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'occupation': request.form['occupation']
	}
	mysql.query_db(query,data)
	return redirect('/')

@app.route('/friends/<id>/edit')
def edit(id):
	# Display the edit friend page for the particular friend
	query = "SELECT * FROM friends WHERE id = {}".format(id)
	friend = mysql.query_db(query)
	session['id'] = friend[0]['id']
	session['first_name'] = friend[0]['first_name']
	session['last_name'] = friend[0]['last_name']
	session['occupation'] = friend[0]['occupation']
	return render_template('edit.html', friend = friend)

@app.route('/friends/<id>', methods=['POST'])
def update(id):
	#Handle the edit friend form submit and update the friend in the DB

	if request.form['first_name'] != "":
		session['first_name'] = request.form['first_name']
	if request.form['last_name'] != "":
		session['last_name'] = request.form['last_name']
	if request.form['occupation'] != "":
		session['occupation'] = request.form['occupation']

	query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, occupation = :occupation WHERE id = :id"
	data = {
		'id': session['id'],
		'first_name': session['first_name'],
		'last_name': session['last_name'],
		'occupation': session['occupation']

	}
	mysql.query_db(query,data)

	session.pop('id')
	session.pop('first_name')
	session.pop('last_name')
	session.pop('occupation')
	return redirect('/')

@app.route('/friends/<id>/delete')
def destroy(id):
	#Delete the friend from the DB
	query = "DELETE FROM friends WHERE id = :id"
	data = {
	'id' : id
	}
	mysql.query_db(query, data)
	return redirect('/')


app.run(debug=True)