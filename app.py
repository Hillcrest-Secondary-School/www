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
    return render_template('admissionpolicy.html')

@app.route('/shool-fees')
def schoolfees():
    return render_template('schoolfees.html')

@app.route('/circulars')
def circulars():
    return render_template('circulars.html')

@app.route('/learners')
def learners():
        return render_template('learners.html')

