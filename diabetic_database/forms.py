from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class registration_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField('Sign Up!')


class login_form(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField('Login')

class health_profile_form(FlaskForm):
    height = StringField("Height:", validators=[DataRequired()])
    weight = StringField("Weight", validators=[DataRequired()])
    age = StringField("Age:", validators=[DataRequired()])
    bmi = StringField("BMI:", validators =[DataRequired()])
    ethnicity = StringField("Ethnicity:", validators=[DataRequired()])
    submit = SubmitField("Create Health Profile!")


