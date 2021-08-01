from typing import List, Dict

import redis
import simplejson as json
from flask import Flask, request, Response, redirect, jsonify, session, render_template_string, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from routes import routes_in_routes

app = Flask(__name__,
            template_folder='../templates')

app.register_blueprint(routes_in_routes)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biostatData.db'

db = SQLAlchemy(app)


class BiostatForm(FlaskForm):
    names = StringField("Name: ")
    sex = StringField("Sex: ")
    age = StringField("Age: ")
    height_in = StringField("Height (inches): ")
    weight_lbs = StringField("Weight (lbs): ")
    submit = SubmitField("Submit")


db.create_all();

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `appl` has been configured
server_session = Session(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)