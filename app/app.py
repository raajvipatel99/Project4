from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'biostatData'
mysql.init_app(app)


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
