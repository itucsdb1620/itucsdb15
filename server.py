import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/culture')
def culture_page():
    now = datetime.datetime.now()
    return render_template('culture.html', current_time=now.ctime())

@app.route('/entertainment')
def entertainment_page():
    entertainment = datetime.datetime.now()
    return render_template('entertainment.html')

@app.route('/landmark')
def landmark_page():
    now = datetime.datetime.now()
    return render_template('landmark.html', current_time=now.ctime())


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
