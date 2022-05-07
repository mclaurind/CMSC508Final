from flask import Flask, render_template, request, flash, redirect, url_for
import pymysql
from forms import registration_form, login_form
from pymysql import connect, cursors


app = Flask(__name__, template_folder= "template")

app.config['SECRET_KEY'] = 'flakjajflkasjfkoasjfoiasjoi'


@app.route("/", methods = ['GET', 'POST'])
def home():

    con = pymysql.connect(
        host = 'cmsc508.com',
        user = 'lodimk2',
        password = 'V00903937',
        database = 'project_lodimk2',
        autocommit = True
    )

    form = registration_form()

    if form.validate_on_submit():
        flash(f'Account Created For {form.username.data}', 'success')
        curs_insert = con.cursor()
        curs_insert.execute(
            'INSERT INTO User_Info(username, password) VALUES ({}, {})'.format("'{}'".format(form.username.data),
                                                                               "'{}'".format(form.password.data)))

        return redirect(url_for('home'))
    curs_select = con.cursor()

    curs_select.execute("select username, password from User_Info")

    out = curs_select.fetchall()
    con.close()
    return render_template('test.html', data = out, form = form)

@app.route("/login")
def login():
    return "<p> PLACEHOLDER </p>"



if __name__ == "__main__":
    app.run(debug=True)


