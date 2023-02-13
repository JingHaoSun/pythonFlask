from flask import Flask, request, render_template, flash
from flask import abort
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'


class NameForm(FlaskForm):
 name = StringField('What is your name?', validators=[])
 submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,  name=session.get('name'), current_time=datetime.utcnow())



@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# @app.route('/user/<id>')
# def get_user(id):
#  user = load_user(id)
#  if not user:
#  abort(404)
#  return '<h1>Hello, {}</h1>'.format(user.name)


# from flask import redirect
# @app.route('/')
# def index():
#  return redirect('http://www.example.com')


# from flask import make_response
# @app.route('/')
# def index():
#  response = make_response('<h1>This document carries a cookie!</h1>')
#  response.set_cookie('answer', '42')
#  return response

# @app.route('/')
# def index():
#  user_agent = request.headers.get('User-Agent')
#  return '<p>Your browser is {}</p>'.format(user_agent)

# @app.route('/')
# def index():
#  return '<h1>Hello World!</h1>'
#
# @app.route('/user/<name>')
# def user(name):
#  return '<h1>Hello, {}!</h1>'.format(name)
