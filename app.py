from flask import *
app = Flask(__name__)
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/studentspace')
def studentspace():
    return render_template('studentspace.html')