from typing import List, Dict

import redis
import simplejson as json
from flask import Flask, request, Response, redirect, jsonify, session, render_template_string, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


app = Flask(__name__,
            template_folder='../templates')



app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biostatData.db'

db = SQLAlchemy(app)


class Biostat(db.Model):
    __tablename__ = 'biostat'
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(20), unique=False, nullable=False)
    sex = db.Column(db.String(3), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    height_in = db.Column(db.Integer, unique=False, nullable=False)
    weight_lbs = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.names



class BiostatForm(FlaskForm):
    names = StringField("Name: ")
    sex = StringField("Sex: ")
    age = StringField("Age: ")
    height_in = StringField("Height (inches): ")
    weight_lbs = StringField("Weight (lbs): ")
    submit = SubmitField("Submit")


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Biostat Project'}
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('index.html', title='Home', user=user, biostat=biostat)


@app.route('/view/<int:biostat_id>', methods=['GET'])
def record_view(biostat_id):
    # print(db.session.query().filter_by(id=address_id).first())
    print(Biostat.query.get(biostat_id).names)
    return render_template('view.html', title='View Form', biostat=Biostat.query.get(biostat_id))


@app.route('/edit/<int:biostat_id>', methods=['GET'])
def form_edit_get(biostat_id):
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    return render_template('edit.html', title='Edit Form', biostat=biostat)


@app.route('/edit/<int:biostat_id>', methods=['POST'])
def form_update_post(biostat_id):
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = request.form.get('names')
    biostat.sex = request.form.get('sex')
    biostat.age = request.form.get('age')
    biostat.height_in = request.form.get('height_in')
    biostat.weight_lbs = request.form.get('weight_lbs')
    db.session.flush()
    db.session.commit()
    return redirect("/", code=302)


@app.route('/biostat/new', methods=['POST'])
def form_insert_get():
    form = BiostatForm()
    biostat = Biostat(names=form.names.data, sex=form.sex.data, age=form.age.data,
                      height_in=form.height_in.data, weight_lbs=form.weight_lbs.data)
    print(biostat.weight_lbs)
    names = form.names
    db.session.add(biostat)
    db.session.commit()
    #remove
    form.names.data = ''
    form.sex.data = ''
    form.age.data = ''
    form.height_in.data = ''
    form.weight_lbs.data = ''
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('new.html', title='New Biostat Form', form=form, names=names, biostat=biostat)


@app.route('/biostat/new', methods=['GET'])
def form_insert_post():
    form = BiostatForm()
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('new.html', title='New Biostat Form', form=form, biostat=biostat)
    return redirect("/", code=302)


@app.route('/delete/<int:biostat_id>', methods=['POST'])
def form_delete_post(biostat_id):
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    print(biostat.age)
    db.session.delete(biostat)
    db.session.commit();
    return redirect("/", code=302)


@app.route('/api/v1/biostat', methods=['GET'])
def api_browse() -> str:
    resp = Biostat.query.all()
    json_res = []
    for temp in resp:
        json_res.append(temp.toDict())
    return jsonify(json_res)


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['GET'])
def api_retrieve(biostat_id) -> str:
    resp = Biostat.query.filter_by(id=biostat_id).one()
    return jsonify(resp.toDict())


@app.route('/api/v1/biostat', methods=['POST'])
def api_add() -> str:
    content = request.json
    biostat = Biostat(names=content['names'], sex=content['sex'], age=content['age'],
                 height_in=content['height_in'], weight_lbs=content['weight_lbs'])
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['PUT'])
def api_edit(biostat_id) -> str:
    content = request.json
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = content['names']
    biostat.sex = content['sex']
    biostat.age = content['age']
    biostat.height_in = content['height_in']
    biostat.weight_lbs = content['weight_lbs']
    resp = Response(status=200, mimetype='application/json')
    return resp
    #here,change content


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['DELETE'])
def api_delete(biostat_id) -> str:
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    # resp = Response(status=200, mimetype='application/json')
    # return resp
    return biostat

db.create_all();

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Create and initialize the Flask-Session object AFTER `app` has been configured
server_session = Session(app)


@app.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':
        # Save the form data to the session object
        session['email'] = request.form['email_address']
        return redirect(url_for('get_email'))

    return """
        <form method="post">
            <label for="email">Enter your email address:</label>
            <input type="email" id="email" name="email_address" required />
            <button type="submit">Submit</button
        </form>
        """


@app.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
            {% endif %}
        """)


@app.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
