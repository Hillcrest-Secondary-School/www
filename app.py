from flask import *
import flask_login
from werkzeug import *
from os import *
import flask_login
import sqlite3
from flask_wtf import *
from wtforms import *
from wtforms.validators import *


app = Flask(__name__)
app.config['UPLOAD_FOLDER']='circulars'
app.config['SECRET_KEY'] = '19edda58164ffd609f09e7c8eb8cb46b'

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    def validate_email(self, email):
        conn = sqlite3.connect('database.sqlite')
        curs = conn.cursor()
        curs.execute("SELECT email FROM login where username = (?)",[email.data])
        valemail = curs.fetchone()
        if valemail is None:
            raise ValidationError('This User ID is not registered. Please register before login')

login_manager = flask_login.LoginManager(app)
login_manager.login_view = "login"
class User(flask_login.UserMixin):
    def __init__(self, id, username, password):
         self.id = id
         self.username = username
         self.password = password
         self.authenticated = False
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

@login_manager.user_loader
def load_user(user_id):
   conn = sqlite3.connect('database.sqlite')
   curs = conn.cursor()
   curs.execute("SELECT * from login where learner_id = (?)",[user_id])
   lu = curs.fetchone()
   if lu is None:
      return None
   else:
      return User(int(lu[0]), lu[1], lu[2])

@app.route("/login", methods=['GET','POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('database.sqlite')
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where username = (?)",    [form.username.data])
        user = list(curs.fetchone())
        Us = load_user(user[0])
        if form.username.data == Us.username and form.password.data == Us.password:
            login_user(Us, remember=form.remember.data)
            Uusername = list({form.username.data})[0].split('@')[0]
            flash('Logged in successfully '+Uusername)
            redirect(url_for('index'))
        else:
            flash('Login Unsuccessfull.')
    return render_template('login.html',title='Login', form=form)

@app.route('/')
def index():
    return render_template('index.html', footer=True)

@app.route('/subject-choices')
def subjectchoices():
    return render_template('subjectchoices.html', footer=True)

@app.route('/admission-policy')
def admissionpolicy():
    return render_template('admissionpolicy.html', footer=True)

@app.route('/shool-fees')
def schoolfees():
    return render_template('schoolfees.html', footer=True)

@app.route('/circulars')
def circulars():
    circulardir = [f for f in listdir(path.join(app.root_path, app.config['UPLOAD_FOLDER'])) if path.isfile(path.join(app.root_path, app.config['UPLOAD_FOLDER'], f))]
    return render_template('circulars.html', footer=True, circulardir=circulardir)

@app.route('/circulars/<path:filename>', methods = ['GET', 'POST'])
def download(filename):
    full_path = path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(full_path, filename)

@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(path.join(app.config['UPLOAD_FOLDER'], f.filename))
      
      return render_template('upload.html', success=True)

@app.route('/learners')
def learners():
        return render_template('learners.html')

@app.route('/class-notes')
def notes():
    return render_template('notes.html')

@app.route('/school-calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/contact-a-teacher')
def contact():
    return render_template('contact.html')

@app.route('/curriculum')
def curriculum():
    return render_template('curriculum.html')