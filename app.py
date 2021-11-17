from flask import *
from werkzeug import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subject-choices')
def subjectchoices():
    return render_template('subjectchoices.html')

@app.route('/admission-policy')
def admissionpolicy():
    return render_template('admissionpolicy.html')

@app.route('/shool-fees')
def schoolfees():
    return render_template('schoolfees.html')

@app.route('/circulars')
def circulars():
    return render_template('circulars.html')
@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(f.filename)
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
    render_template('contact.html')

@app.route('/curriculum')
def curriculum():
    return render_template('curriculum.html')