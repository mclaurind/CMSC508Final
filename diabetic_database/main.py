from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import *
import pymysql
username = "Placeholder"
password = "Placeholder"
app = Flask(__name__)


app.config['SECRET_KEY'] = "oiwehfiojfiojdsofijsidof"

@app.route("/", methods = ["POST", "GET"])
def index():
    global username
    global password
    form = login_form()
    try:
        if form.validate_on_submit():
            con = pymysql.connect(
                host='cmsc508.com',
                user='lodimk2',
                password='V00903937',
                database='project_lodimk2',
                autocommit=True
            )
            curs_user = con.cursor()
            curs_pass = con.cursor()
            form = login_form()
            curs_user.execute("SELECT username from User_Info WHERE username = {}".format("'{}'".format(form.username.data)))
            curs_pass.execute("SELECT password from User_Info WHERE username = {}".format("'{}'").format(form.username.data))
            sql_pass = curs_pass.fetchall()
            if sql_pass[0][0] == form.password.data:
                username = form.username.data
                password = form.password.data
                flash(f'Logged into {username}!', 'success')
                return redirect(url_for('profile'))
            else:
                flash("Please try again! Invalid Login Credentials")
    except IndexError:
        flash("Please enter a valid username, or sign up!")
    return render_template('index.html', form = form)

@app.route("/profile", methods = ["POST", "GET"])
def profile():

    con = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )
    form = health_profile_form()
    con_select = con.cursor()
    con_select.execute("SELECT * FROM Health_Profile WHERE username = {}".format("'{}'").format(username))

    select_results = con_select.fetchone()
    message_str = ""
    for item in select_results:
        message_str += str(item) + " "

    print(message_str)
    message = message_str
    return render_template('health_profile.html', form = form, message = message, username = username)


@app.route("/signup", methods = ["POST", "GET"])
def signup():
    form = registration_form()
    try:
        if form.validate_on_submit():
            con = pymysql.connect(
                host='cmsc508.com',
                user='lodimk2',
                password='V00903937',
                database='project_lodimk2',
                autocommit=True
            )
            con_insert = con.cursor()
            con_insert.execute("INSERT INTO User_Info(username, password) VALUES ({}, {})".format("'{}'".format(form.username.data),"'{}'".format(form.password.data)))
            flash(f"Successfully added user {form.username.data}", "success")
            return redirect(url_for("index"))
    except pymysql.err.IntegrityError:
        flash("This user already exists, please choose a new username", "danger")

    return render_template("signup.html", form = form)



