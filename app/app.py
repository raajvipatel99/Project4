from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
# from flaskext.mysql import MySQL
# from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField
from flask_wtf import FlaskForm


app = Flask(__name__)
# mysql = MySQL(cursorclass=DictCursor)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/biostatData.db'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(20), unique=False, nullable=False)
    sex = db.Column(db.String(5), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    height_in = db.Column(db.Integer, unique=False, nullable=False)
    weight_lbs = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class UserForm(FlaskForm):
    name = StringField("Name: ")
    sex = StringField("Sex: ")
    age = StringField("Age: ")
    height_in = StringField("Height (inches): ")
    weight_lbs = StringField("Weight (lbs): ")


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Biostat Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostat')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, biostat=result)


@app.route('/view/<int:biostat_id>', methods=['GET'])
def record_view(biostat_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostat WHERE id=%s', biostat_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', biostat=result[0])


@app.route('/edit/<int:biostat_id>', methods=['GET'])
def form_edit_get(biostat_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostat WHERE id=%s', biostat_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', biostat=result[0])


@app.route('/edit/<int:biostat_id>', methods=['POST'])
def form_update_post(biostat_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('names'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'),biostat_id)
    sql_update_query = """UPDATE biostat t SET t.names = %s, t.sex = %s, t.age = %s, t.height_in = 
    %s, t.weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

# hereeeeee
@app.route('/biostat/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Biostat Form')

# hereeeeee
@app.route('/biostat/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('names'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'))
    sql_insert_query = """INSERT INTO biostat (names,sex,age,height_in,weight_lbs) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:biostat_id>', methods=['POST'])
def form_delete_post(biostat_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostat WHERE id = %s """
    cursor.execute(sql_delete_query, biostat_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/biostat', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostat')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['GET'])
def api_retrieve(biostat_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM biostat WHERE id=%s', biostat_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostat', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('names'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'))
    sql_insert_query = """INSERT INTO biostat (names,sex,age,height_in,weight_lbs) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['PUT'])
def api_edit(biostat_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (request.form.get('names'), request.form.get('sex'), request.form.get('age'),
                 request.form.get('height_in'), request.form.get('weight_lbs'), biostat_id)
    sql_update_query = """UPDATE biostat t SET t.names = %s, t.sex = %s, t.age = %s, t.height_in = 
       %s, t.weight_lbs = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/biostat/<int:biostat_id>', methods=['DELETE'])
def api_delete(biostat_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM biostat WHERE id = %s """
    cursor.execute(sql_delete_query, biostat_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
