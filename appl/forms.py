from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class BiostatForm(FlaskForm):
    names = StringField("Name: ")
    sex = StringField("Sex: ")
    age = StringField("Age: ")
    height_in = StringField("Height (inches): ")
    weight_lbs = StringField("Weight (lbs): ")
    submit = SubmitField("Submit")

class SignupForm(FlaskForm):
    username = StringField("Username: ")
    password = StringField("Password: ")
    signup = SubmitField("Signup")
