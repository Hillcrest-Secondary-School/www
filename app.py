'''
@author: Wessel Steenkamp

@version: v0.1
@maintainer: Wessel Steenkamp
@email: wessel.steenkamp@gmail.com
@status: beta
'''

from os import *
import re
from functools import wraps
import sqlite3
from flask import *
import flask_login
from flask_login.utils import login_required
from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from werkzeug import *

# Defines the configuration of the web application. Do not make the secret key public.
app = Flask(__name__)
app.config['UPLOAD_FOLDER']='circulars'
app.config['SECRET_KEY'] = '19edda58164ffd609f09e7c8eb8cb46b'   # Secret key. Not to be made public.

# General login form for the web application.
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    def validate_username(self, username):
        conn = sqlite3.connect('database.sqlite')
        curs = conn.cursor()
        curs.execute("SELECT UserName FROM login WHERE UserName = (?)",[username.data])
        valusername = curs.fetchone()
        if valusername is None:
            raise ValidationError('This User ID is not registered. Please register before login')

login_manager = flask_login.LoginManager(app)
login_manager.login_view = "login"

# Defines access levels of the application.
LEVEL = {
    'user':0,
    'admin':1
    }

# Defines the user class and all of the info paired with the users.
# The sqlite3 database is used to store all info related to users.
class User(flask_login.UserMixin):
    def __init__(self, id, username, password, level):
         self.id = id
         self.username = username
         self.password = password
         self.authenticated = False
         self.is_admin = False
         if level == LEVEL['admin']:
             self.is_admin = True

    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
    def allowed(self, access_level):
        return self.is_admin >= access_level

# Basic user loader to load users on the application's session.
@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('database.sqlite')
   curs = conn.cursor()
   curs.execute("SELECT * FROM login WHERE ID = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
        return None
   else:
        return User(int(lu[0]), lu[1], lu[2], lu[3])

# URL Endpoint for logging in to the application.
@app.route("/login", methods=['GET','POST'])
def login():
    if flask_login.current_user.is_authenticated:
        if flask_login.current_user.is_admin:
            return redirect(url_for('teachers'))
        else:
            return redirect(url_for('learners'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('database.sqlite')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login WHERE UserName = (?)",    [form.username.data])
        user = curs.fetchone()
        Us = load_user(user[0])
        if form.username.data == Us.username and form.password.data == Us.password:
            flask_login.login_user(Us, remember=form.remember.data)
            Uusername = form.username.data
            flash('Logged in successfully '+Uusername)
            redirect(url_for('index'))
        else:
            flash('Login Unsuccessfull.')
    return render_template('login.html',title='Login', form=form)

# URL Endpoint for logging out of the application.
@app.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

# Defines the decorator for admin-only pages.
# Used with @ to every endpoint that only allows admin.
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        try:
            if not flask_login.current_user.is_admin:
                return current_app.login_manager.unauthorized()
        except:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

'''
This section of the website is dedicated to the public.
Here people should find general infomation about the school.
'''

# Landing page of the application.
@app.route('/')
def index():
    return render_template('index.html', footer=True)

# Info about subject choices at the school.
@app.route('/subject-choices')
def subjectchoices():
    return render_template('subjectchoices.html', footer=True)

# Info about the admission policy of the school.
@app.route('/admission-policy')
def admissionpolicy():
    return render_template('admissionpolicy.html', footer=True)

# Info about the school fees of the schools.
@app.route('/shool-fees')
def schoolfees():
    return render_template('schoolfees.html', footer=True)

# All of the circulars of the school, managed by the /teachers/upload_circular URL Endpoint.
@app.route('/circulars')
def circulars():
    circulardir = [f for f in listdir(path.join(app.root_path, app.config['UPLOAD_FOLDER'])) if path.isfile(path.join(app.root_path, app.config['UPLOAD_FOLDER'], f))]
    return render_template('circulars.html', footer=True, circulardir=circulardir)

# Downloader of the circulars.
@app.route('/circulars/<path:filename>', methods = ['GET', 'POST'])
def download(filename):
    full_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(full_path, filename)

'''
This section of the website is dedicated to the learners.
Here they can view their notes and grades.
'''

# Dashboard of the learners.
@app.route('/learners')
def learners():
    return render_template('learners.html')

# Class notes of learners.
@app.route('/learners/class-notes')
@login_required
def notes():
    return render_template('notes.html')

# Google calendar of the school.
# IMPORTANT: The calendar needs an active internet connection to load.
@app.route('/learners/school-calendar')
@login_required
def calendar():
    return render_template('calendar.html')

# Contact details of a learner's teacher.
@app.route('/learners/contact-a-teacher')
@login_required
def contact():
    return render_template('contact.html')

# Curriculum and lesson plans of the learners.
@app.route('/learners/curriculum')
@login_required
def curriculum():
    return render_template('curriculum.html')

'''
This section of the website is dedicated to the teachers.
Here they can manage the profiles and grades of the learners.
'''

# Dashboard of the teachers. Replaces the learner's dashboard.
@app.route('/teachers')
@admin_required
def teachers():
    return render_template('teachers.html')

# Manages the grades of the learners.
@app.route('/teachers/grades')
@admin_required
def teacher_grades():
    return render_template('teacher_grades.html')

# URL Endpoint for choosing which circular to upload.
@app.route('/teacher/upload-circular')
@admin_required
def upload_circular():
   return render_template('upload.html')

# Uploads the circular to the server and makes it availible for download at /circulars.
@app.route('/teacher/uploader-circular', methods = ['GET', 'POST'])
@admin_required
def uploader_cicrular():
   if request.method == 'POST':
      f = request.files['file']
      f.save(path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
      return render_template('upload.html', success=True)