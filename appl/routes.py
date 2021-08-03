from functools import wraps

from flask import Blueprint, request, session, redirect, url_for, render_template_string, render_template, Response, \
    jsonify

routes_in_routes = Blueprint('routes_in_routes', __name__)


@routes_in_routes.before_app_first_request
def prefill_db():
    from app import db
    from models import Biostat
    db.session.query(Biostat).delete()
    db.session.commit()
    try:
        for csv_row in open("../db/init.csv", "r"):
            line = csv_row.strip().split(",")
            print(line)
            names = line[0]
            sex = line[1]
            age = line[2]
            height_in = line[3]
            weight_lbs = line[4]
            b = Biostat(names=names, sex=sex, age=age, height_in=height_in, weight_lbs=weight_lbs)
            db.session.add(b)
            db.session.commit()
    except:
        print("out")
    finally:
        print("in")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') is None:
            return redirect(url_for('routes_in_routes.get_email'), code=302)
        return f(*args, **kwargs)

    return decorated_function


@routes_in_routes.route('/', methods=['GET'])
@login_required
def index():
    from appl.models import Biostat
    user = {'username': 'Biostat Project'}
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('index.html', title='Home', user=user, biostat=biostat)


@routes_in_routes.route('/view/<int:biostat_id>', methods=['GET'])
@login_required
def record_view(biostat_id):
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    # print(db.session.query().filter_by(id=address_id).first())
    print(Biostat.query.get(biostat_id).names)
    return render_template('view.html', title='View Form', biostat=Biostat.query.get(biostat_id))


@routes_in_routes.route('/edit/<int:biostat_id>', methods=['GET'])
@login_required
def form_edit_get(biostat_id):
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    return render_template('edit.html', title='Edit Form', biostat=biostat)


@routes_in_routes.route('/edit/<int:biostat_id>', methods=['POST'])
@login_required
def form_update_post(biostat_id):
    from app import db
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = request.form.get('names')
    biostat.sex = request.form.get('sex')
    biostat.age = request.form.get('age')
    biostat.height_in = request.form.get('height_in')
    biostat.weight_lbs = request.form.get('weight_lbs')
    # print(biostat.weight_lbs)
    db.session.flush()
    db.session.commit()
    return redirect("/", code=302)


@routes_in_routes.route('/biostat/new', methods=['POST'])
@login_required
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
@login_required
def form_insert_post():
    from appl.app import db
    from appl.forms import BiostatForm
    from appl.models import Biostat
    form = BiostatForm()
    biostat = Biostat.query.order_by(Biostat.id)
    return render_template('new.html', title='New Biostat Form', form=form, biostat=biostat)
    return redirect("/", code=302)


@routes_in_routes.route('/delete/<int:biostat_id>', methods=['POST'])
@login_required
def form_delete_post(biostat_id):
    from app import db
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    # print(biostat.age)
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
    db.session.add(biostat)
    db.session.commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@routes_in_routes.route('/api/v1/biostat/<int:biostat_id>', methods=['PUT'])
def api_edit(biostat_id) -> str:
    from appl.app import db
    from appl.models import Biostat
    from flask import request, Response
    content = request.json
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    biostat.names = content['names']
    biostat.sex = content['sex']
    biostat.age = content['age']
    biostat.height_in = content['height_in']
    biostat.weight_lbs = content['weight_lbs']
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp



@routes_in_routes.route('/api/v1/biostat/<int:biostat_id>', methods=['DELETE'])
def api_delete(biostat_id) -> str:
    from app import db
    from appl.models import Biostat
    biostat = Biostat.query.filter_by(id=biostat_id).one()
    db.session.delete(biostat)
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@routes_in_routes.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'POST':


        from appl.models import Signup
        username = request.form['username']
        password = request.form['password']
        user_obj = Signup.query.filter_by(username=username).first()
        if user_obj is not None:
            if username == user_obj.username and password == user_obj.password:
                session['email'] = request.form['username']
                return redirect(url_for('routes_in_routes.index'))
            else:
                return render_template_string("""
                    Invalid Password. Please try again!
                    <h3><a href="{{ url_for('routes_in_routes.get_email') }}">Back</a></h3>
                """)
        else:
            return render_template_string("""
                                Username not found!
                                 <h3><a href="{{ url_for('routes_in_routes.get_email') }}">Back</a></h3>
                            """)



        #return redirect(url_for('routes_in_routes.get_email'))

    return """
        <form method="post">
            <label for="email">Username:</label>
            <input type="username" id="username" name="username" required />
             <label for="password">Password:</label>
            <input type="password" id="password" name="password" required />  
            <button type="submit">Submit</button
        </form>
        """
    # if request.method == 'POST':
    #     session['email'] = request.form['email_address']
    #     return redirect(url_for('routes_in_routes.get_email'))
    #
    # return """
    #        <form method="post">
    #            <label for="email">Enter your email address:</label>
    #            <input type="email" id="email" name="email_address" required />
    #            <button type="submit">Submit</button
    #        </form>
    #        """

# uselessssssssssss--------------------------------
# @routes_in_routes.route('/get_email', methods=['GET', 'POST'])
# def get_email():
#     from appl.app import db
#     from appl.forms import SignupForm
#     from appl.models import Signup
#     sform = SignupForm()
#     username = sform.username.data
#     password = sform.password.data
#     user_obj = Signup.query.filter_by(username=username).one()
#     if username == user_obj.username and password == user_obj.password:
#         return redirect(url_for('routes_in_routes.index'))
#     else:
#         return render_template_string("""
#          <h1>Welcome! <h1>
#          <h2> <a href="{{ url_for('routes_in_routes.set_email') }}">Login</a></h>
#          <h2><a href="{{ url_for('routes_in_routes.signup') }}">Signup</a></h2>
#         """)



@routes_in_routes.route('/get_email')
def get_email():
    return render_template_string("""
            {% if session['email'] %}
                <h1> <a href="{{ url_for('routes_in_routes.index') }}">Go to HomePage</a> </h1>
            {% else %}
                <h1>Welcome! <h1>
                <h2> <a href="{{ url_for('routes_in_routes.set_email') }}">Login</a></h>
                <h2><a href="{{ url_for('routes_in_routes.signup') }}">Signup</a></h2>
            {% endif %}
        """)


@routes_in_routes.route('/delete_email')
def delete_email():
    # Clear the email stored in the session object
    session.pop('email', default=None)
    return '<h1>Session deleted!</h1>'


@routes_in_routes.route('/signup', methods=['POST', 'GET'])
def signup():
    print("hey")
    from appl.app import db
    from appl.forms import SignupForm
    from appl.models import Signup
    form = SignupForm()
    reg = Signup(username=form.username.data, password=form.password.data)
    username = form.username
    db.session.add(reg)
    db.session.commit()
    form.username.data = ''
    form.password.data = ''
    reg = Signup.query.order_by(Signup.id)
    return render_template('signup.html', title='Signup Form', form=form, username=username, reg=reg)
