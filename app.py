from flask import *
app = Flask(__name__)
@app.route('/')
def index():
  retrun render_template('index.html')
