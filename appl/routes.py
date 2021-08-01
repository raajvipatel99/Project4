from flask import Blueprint, request, session, redirect, url_for, render_template_string, render_template, Response, \
    jsonify

routes_in_routes = Blueprint('routes_in_routes', __name__)


@routes_in_routes.route('/', methods=['GET'])
def index():
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    user = {'username': 'Biostat Project'}
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('index.html', title='Home', user=user, biostat=biostat)


@routes_in_routes.route('/view/<int:biostat_id>', methods=['GET'])
def record_view(biostat_id):
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    # print(db.session.query().filter_by(id=address_id).first())
    print(Biostat.query.get(biostat_id).names)
    return render_template('view.html', title='View Form', biostat=Biostat.query.get(biostat_id))


@routes_in_routes.route('/edit/<int:biostat_id>', methods=['GET'])
def form_edit_get(biostat_id):
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    return render_template('edit.html', title='Edit Form', biostat=biostat)


@routes_in_routes.route('/edit/<int:biostat_id>', methods=['POST'])
def form_update_post(biostat_id):
    from app import db
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = request.form.get('names')
    biostat.sex = request.form.get('sex')
    biostat.age = request.form.get('age')
    biostat.height_in = request.form.get('height_in')
    biostat.weight_lbs = request.form.get('weight_lbs')
    #print(biostat.weight_lbs)
    db.session.flush()
    db.session.commit()
    return redirect("/", code=302)


@routes_in_routes.route('/biostat/new', methods=['POST'])
def form_insert_get():
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    form = BiostatForm()
    biostat = Biostat(names=form.names.data, sex=form.sex.data, age=form.age.data,
                      height_in=form.height_in.data, weight_lbs=form.weight_lbs.data)
    print(biostat.weight_lbs)
    names = form.names
    db.session.add(biostat)
    db.session.commit()
    # remove
    form.names.data = ''
    form.sex.data = ''
    form.age.data = ''
    form.height_in.data = ''
    form.weight_lbs.data = ''
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('new.html', title='New Biostat Form', form=form, names=names, biostat=biostat)


@routes_in_routes.route('/biostat/new', methods=['GET'])
def form_insert_post():
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    form = BiostatForm()
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('new.html', title='New Biostat Form', form=form, biostat=biostat)
    return redirect("/", code=302)


@routes_in_routes.route('/delete/<int:biostat_id>', methods=['POST'])
def form_delete_post(biostat_id):
    from app import db
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    #print(biostat.age)
    db.session.delete(biostat)
    db.session.commit()
    return redirect("/", code=302)


@routes_in_routes.route('/api/v1/biostat', methods=['GET'])
def api_browse() -> str:
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    resp = Biostat.query.all()
    json_res = []
    for temp in resp:
        json_res.append(temp.toDict())
    return jsonify(json_res)


@routes_in_routes.route('/api/v1/biostat/<int:biostat_id>', methods=['GET'])
def api_retrieve(biostat_id) -> str:
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    resp = Biostat.query.filter_by(id=biostat_id).one()
    return jsonify(resp.toDict())


@routes_in_routes.route('/api/v1/biostat', methods=['POST'])
def api_add() -> str:
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    content = request.json
    biostat = Biostat(names=content['names'], sex=content['sex'], age=content['age'],
                      height_in=content['height_in'], weight_lbs=content['weight_lbs'])
    resp = Response(status=201, mimetype='application/json')
    return resp


@routes_in_routes.route('/api/v1/biostat/<int:biostat_id>', methods=['PUT'])
def api_edit(biostat_id) -> str:
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    content = request.json
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = content['names']
    biostat.sex = content['sex']
    biostat.age = content['age']
    biostat.height_in = content['height_in']
    biostat.weight_lbs = content['weight_lbs']
    resp = Response(status=200, mimetype='application/json')
    return resp
    # here,change content


@routes_in_routes.route('/api/v1/biostat/<int:biostat_id>', methods=['DELETE'])
def api_delete(biostat_id) -> str:
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    # resp = Response(status=200, mimetype='application/json')
    # return resp
    return biostat


@routes_in_routes.route('/set_email', methods=['GET', 'POST'])
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


@routes_in_routes.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1>Welcome! Please enter your email <a href="{{ url_for('set_email') }}">here.</a></h1>
            {% endif %}
        """)


@routes_in_routes.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'
