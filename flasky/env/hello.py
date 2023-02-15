import os

from flask import Flask, request, render_template, flash
from flask import abort
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms.validators import DataRequired
from gevent import pywsgi
from flask_mail import Mail




app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

#数据库配置sqllite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#数据库迁移
migrate = Migrate(app, db)

#配置Gmail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# server = pywsgi.WSGIServer(('0.0.0.0', 12345), app)
# server.serve_forever()


class NameForm(FlaskForm):
 name = StringField('What is your name?', validators=[])
 submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role',lazy='dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        #变更名字提示
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')

        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    #current_time(时间显示)
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),current_time=datetime.utcnow())


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

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
