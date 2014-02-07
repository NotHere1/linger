from flask import Flask, jsonify, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import requests, os
import models
from sqlalchemy import create_engine

app = Flask(__name__)
app.debug = True

#app.config['SQLALCHEMY_ECHO'] = True
app.config.from_object('config.flask_config')
db = SQLAlchemy(app)


@app.route("/")
def login():
	return render_template("login.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if request.method == "POST":
		print 'signup-post'
		return render_template("signup.html", signup_email=request.form["register_email"])
	else: # request.method == "GET"
		print 'signup-get'
		return render_template("signup.html")

@app.route("/signup-submit", methods=["GET", "POST"])

def signup_submit():
	#request_form...
	if request.method == "POST":
		print 'signupsubmit-post'
		# add method to get elements from post and push to db.
		# js alert? homepage?
		#check equal passwords
		if request.form['signup-pass1'] == request.form['signup-pass1']:
			new_user = models.User(
					request.form['signup-name'], 
					request.form['signup-email'], 
					request.form['signup-phone'],
					request.form['signup-pass1'])
			print new_user
			db.session.add(new_user)
			db.session.commit()
			return render_template("signupsuccess.html", signup_email=request.form["register_email"])
		else:
			#TO DO: print 'password incorrect?'
			return render_template("signup.html")
	else: # request.method == "GET"
		print 'signupsubmit-post'
		return render_template("signup.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")


#goal: add username entry from blah.
@app.route('/user/<username_entry>')
def show_user_profile(username_entry):
	''' Show user profile of username, contacts, messages '''
	#query db for user info

	user_instance = models.User.query.filter_by(user_name=username_entry).first()
	#if user doesn't exist, route to signup page
	if user_instance is None:
		return render_template("signup.html")
	#only displaying if user exists...
	#print 'user_instance', user_instance.user_id
	contact_dict = user_instance.user_contacts.all() 
	inmessages_dict = user_instance.user_inmessages.all()
	outmessages_dict = user_instance.user_outmessages.all()

	print 'USERNAME INSTANCE: ', user_instance
	print 'CONTACT: ', contact_dict
	print 'MESSAGES: ', inmessages_dict, outmessages_dict
	
	#render template w/ contacts, messages in dictionary form
	return render_template("dashboard.html", 
		username= username_entry, 
		contacts = contact_dict, 
		inmessages = inmessages_dict,
		outmessages = outmessages_dict)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
	app.run(host="0.0.0.0")