from flask import *
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subject-choices')
def subjectchoices():
    return render_template('subjectchoices.html')

@app.route('/admission-policy')
def admissionpolicy():
    return 'Admission Policy'

@app.route('/shool-fees')
def schoolfees():
    return 'School Fees'

@app.route('/circulars')
def circulars():
    return 'Circulars'

@app.route('/learners')
def studentspace():
        return render_template('learners.html')

