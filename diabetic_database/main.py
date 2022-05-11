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
    headers = ["Username", "Height", "Weight", "Age", "BMI", "Ethnicity"]
    select_results = con_select.fetchone()
    out_message = ""
    if select_results == None:
        check = True
        form_header = "Create your health profile!"
        out_message = "Your health profile will be displayed here"
    else:
        print(select_results)
        check = False
        form_header = "Update your health profile!"

    if form.validate_on_submit():
        con_insert = con.cursor()
        if form_header == "Create your health profile!":
                sql_str = f"INSERT INTO Health_Profile (username,height,weight,age,bmi,ethnicity) VALUES ('{username}', {form.height.data}, {form.weight.data}, {form.age.data}, {form.bmi.data}, '{form.ethnicity.data}')"
                print(sql_str)
                con_insert.execute(sql_str)
        else:
            sql_str = f"UPDATE Health_Profile SET height = {form.height.data},weight = {form.weight.data},age = {form.age.data},bmi = {form.bmi.data},ethnicity = '{form.ethnicity.data}' WHERE username = '{username}'"
            con_insert.execute(sql_str)



            return redirect(url_for("profile"))




    return render_template('health_profile.html', form = form, out_message = out_message, username = username, form_header = form_header, select_results = select_results, headers = headers, check = check)


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
            flash(f" Account created for {form.username.data}", "success")
            return redirect(url_for("index"))
    except pymysql.err.IntegrityError:
        flash("This user already exists, please choose a new username", "danger")

    return render_template("signup.html", form = form)
@app.route("/events", methods = ["POST", "GET"])
def entry_page():
    entry_options = ["Exercise", "Food", "Medicine", "Blood_Sugar"]
    headers = ["Username", "Event_Type","Time"]

    option = ""
    form = starter_entry_form()

    con = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )

    con_select = con.cursor()

    sql_select = f"SELECT username, event_type, event_time FROM User_Event WHERE username = '{username}' ORDER BY event_time"

    con_select.execute(sql_select)

    message = con_select.fetchall()

    if form.validate_on_submit():
        option = form.myField.data
        redirect_str =f"{option}"
        return redirect(url_for(redirect_str.lower()))

    return render_template('entry.html', options = entry_options, form = form, headers = headers, message = message)
@app.route("/food", methods = ["POST", "GET"])
def food():
    con_one = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )
    con_one_foodtable = con_one.cursor()
    form = food_form()
    food_table_str = f"SELECT u.username, u.event_time, f.name, f.carbs FROM User_Event u JOIN Food f ON u.food_id = f.food_id WHERE username = '{username}'"
    con_one_foodtable.execute(food_table_str)

    headers = ["Username", "Event_Time", "Food_Name", "Carbs"]
    global message
    message = con_one_foodtable.fetchall()
    con_one.close()
    if form.validate_on_submit():
        con = pymysql.connect(
            host='cmsc508.com',
            user='lodimk2',
            password='V00903937',
            database='project_lodimk2',
            autocommit=True
        )
        con_get = con.cursor()
        con_insert = con.cursor()
        con_entry = con.cursor()
        con_select = con.cursor()

        get_sql = "SELECT name FROM Food"
        con_get.execute(get_sql)
        food_names_big = con_get.fetchall()
        food_names = []




        for item in range(len(food_names_big[0])):
            print(food_names_big[item][0])
            food_names.append(food_names_big[item][0])
        print(food_names)


        if form.name.data not in food_names:
            print("Made it here!")
            sql_string = f"INSERT INTO Food (name,carbs) VALUES ('{form.name.data}', {form.carbs.data})"
            con_insert.execute(sql_string)
            sql_select = f"SELECT food_id FROM Food WHERE name = '{form.name.data}'"
            con_select.execute(sql_select)
            select_result = con_select.fetchone()

            food_id = select_result[0]
            sql_insert_str = f"INSERT INTO User_Event(username, food_id, event_type, event_time) VALUES ('{username}',{food_id},'Food', CURRENT_TIMESTAMP())"
            print(sql_insert_str)
            con_insert.execute(sql_insert_str)
            con.close()
            return redirect(url_for("entry_page"))
        else:
            print("I am here")
            sql_select = f"SELECT food_id FROM Food WHERE name = '{form.name.data}'"
            con_select.execute(sql_select)
            select_result = con_select.fetchone()

            food_id = select_result[0]
            sql_insert_str = f"INSERT INTO User_Event(username, food_id, event_type, event_time) VALUES ('{username}',{food_id},'Food',CURRENT_TIMESTAMP())"
            con_insert.execute(sql_insert_str)
            con.close()
            return redirect(url_for("entry_page"))

    return render_template("food.html", form = form, message = message, headers = headers)

@app.route("/blood_sugar", methods = ["POST", "GET"])
def blood_sugar():
    form = blood_sugar_form()

    con_one = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )
    con_one_blood_sugar = con_one.cursor()

    bg_str = f"SELECT u.username, u.event_time, b.number FROM User_Event u JOIN Blood_Sugar b ON b.blood_sugar_id = u.blood_sugar_id WHERE username = '{username}'"
    con_one_blood_sugar.execute(bg_str)

    headers = ["Username", "Event Time", "Blood Sugar"]
    message = con_one_blood_sugar.fetchall()
    con_one.close()

    if form.validate_on_submit():
        con = pymysql.connect(
            host='cmsc508.com',
            user='lodimk2',
            password='V00903937',
            database='project_lodimk2',
            autocommit=True
        )
        con_insert_bg = con.cursor()
        con_insert_user = con.cursor()
        con_get = con.cursor()
        bg_insert = f"INSERT INTO Blood_Sugar (number) VALUES ({form.number.data})"
        con_insert_bg.execute(bg_insert)

        sql_select = f"SELECT blood_sugar_id FROM Blood_Sugar WHERE number = '{form.number.data}'"
        con_get.execute(sql_select)
        select_result = con_get.fetchone()
        blood_sugar_id = select_result[0]


        sql_insert_str = f"INSERT INTO User_Event(username, blood_sugar_id,event_type,event_time) VALUES ('{username}',{blood_sugar_id},'Blood Sugar', CURRENT_TIMESTAMP())"
        con_insert_user.execute(sql_insert_str)

        return redirect(url_for("entry_page"))

    return render_template("blood_sugar.html", form = form, message = message, headers = headers)

@app.route("/medicine", methods = ["POST", "GET"])
def medicine():
    form = medicine_form()

    con_one = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )
    con_one_medicine = con_one.cursor()

    med_str = f"SELECT u.username, u.event_time, m.name, m.type, m.dosage FROM User_Event u JOIN Medicine m ON m.medicine_id = u.medicine_id WHERE username = '{username}'"
    con_one_medicine.execute(med_str)

    headers = ["Username", "Event_Time", "Medicine_Name", "Medicine_Type", "Dosage"]
    message = con_one_medicine.fetchall()
    con_one.close()

    if form.validate_on_submit():
        con = pymysql.connect(
            host='cmsc508.com',
            user='lodimk2',
            password='V00903937',
            database='project_lodimk2',
            autocommit=True
        )
        con_insert_med = con.cursor()
        con_insert_user = con.cursor()
        con_get = con.cursor()
        med_insert = f"INSERT INTO Medicine (name, type, dosage) VALUES ('{form.name.data}', '{form.type.data}', {form.dosage.data})"
        con_insert_med.execute(med_insert)

        sql_select = f"SELECT medicine_id FROM Medicine WHERE name = '{form.name.data}'"
        con_get.execute(sql_select)
        select_result = con_get.fetchone()
        medicine_id = select_result[0]


        sql_insert_str = f"INSERT INTO User_Event(username, medicine_id,event_type,event_time) VALUES ('{username}',{medicine_id},'Medicine', CURRENT_TIMESTAMP())"
        con_insert_user.execute(sql_insert_str)

        return redirect(url_for("entry_page"))

    return render_template("medicine.html", form=form, message=message, headers=headers)
@app.route("/exercise", methods = ["POST", "GET"])
def exercise():
    form = exercise_form()

    con_one = pymysql.connect(
        host='cmsc508.com',
        user='lodimk2',
        password='V00903937',
        database='project_lodimk2',
        autocommit=True
    )
    con_one_exercise = con_one.cursor()

    exe_str = f"SELECT u.username, u.event_time, e.type, e.calories_burned, e.duration FROM User_Event u JOIN Exercise e ON e.exercise_id = u.exercise_id WHERE username = '{username}'"
    con_one_exercise.execute(exe_str)

    headers = ["Username", "Event_Time", "Exercise_Type", "Calories_Burned", "Duration"]
    message = con_one_exercise.fetchall()
    con_one.close()

    if form.validate_on_submit():
        con = pymysql.connect(
            host='cmsc508.com',
            user='lodimk2',
            password='V00903937',
            database='project_lodimk2',
            autocommit=True
        )
        con_insert_exe = con.cursor()
        con_insert_user = con.cursor()
        con_get = con.cursor()
        exe_insert = f"INSERT INTO Exercise (type, calories_burned, duration) VALUES ('{form.type.data}', '{form.calories_burned.data}', {form.duration.data})"
        con_insert_exe.execute(exe_insert)

        sql_select = f"SELECT exercise_id FROM Exercise WHERE type = '{form.type.data}'"
        con_get.execute(sql_select)
        select_result = con_get.fetchone()
        exercise_id = select_result[0]

        sql_insert_str = f"INSERT INTO User_Event(username, exercise_id,event_type,event_time) VALUES ('{username}',{exercise_id},'Exercise', CURRENT_TIMESTAMP())"
        con_insert_user.execute(sql_insert_str)

        return redirect(url_for("entry_page"))

    return render_template("exercise.html", form=form, message=message, headers=headers)


@app.route("/logout")
def logout():
    global username
    global password
    username = "PLACEHOLDER"
    password = "PLACEHOLDER"
