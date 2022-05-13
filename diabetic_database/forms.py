from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class registration_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField('Sign Up')

class login_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')

class health_profile_form(FlaskForm):
    height = StringField("Height (in inches):", validators=[DataRequired()])
    weight = StringField("Weight (in lbs)", validators=[DataRequired()])
    age = StringField("Age:", validators=[DataRequired()])
    bmi = StringField("BMI:", validators =[DataRequired()])
    ethnicity = StringField("Ethnicity:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class starter_entry_form(FlaskForm):
    entry_options = ["Exercise", "Food", "Medicine", "Blood_Sugar"]
    #type = StringField("Type:")
    myField = SelectField('Event Type', choices=entry_options, validators=[DataRequired()])
    submit = SubmitField("Submit")

class food_form(FlaskForm):
    name = StringField("Food:",validators=[DataRequired()])
    carbs = StringField("Carbs:",validators=[DataRequired()])
    submit = SubmitField("Submit")

class blood_sugar_form(FlaskForm):

    number = StringField("Blood Sugar Value:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class medicine_form(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    type = StringField("Type:", validators=[DataRequired()])
    dosage = StringField("Dosage:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class exercise_form(FlaskForm):
    type = StringField("Type:", validators=[DataRequired()])
    calories_burned = StringField("Calories Burned:",validators=[DataRequired()])
    duration = StringField("Duration (in minutes):",validators=[DataRequired()])
    submit = SubmitField("Submit")