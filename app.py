from flask import *
from werkzeug import *
from os import *
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='circulars'

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