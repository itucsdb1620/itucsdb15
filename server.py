import datetime
import os
import psycopg2 as dbapi2
import json
import re

from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Culture"""
        cursor.execute(query)

        query = """CREATE TABLE Culture (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE FLOAT
                )"""
        cursor.execute(query)

        query = """INSERT INTO Culture (NAME, SCORE)
                    VALUES ('Cultural Placeholder 1', 8.5),
                           ('Cultural Placeholder 2', 9),
                           ('Cultural Placeholder 3', 7.7)"""
        cursor.execute(query)
        
        query = """DROP TABLE IF EXISTS Entertainment"""
        cursor.execute(query)
        
        query = """CREATE TABLE Entertainment(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                PLACE VARCHAR(255) NULL,
                SCORE FLOAT NULL
                )"""
        cursor.execute(query)
        
        query = """INSERT INTO Entertainment(NAME, PLACE,SCORE)
                    VALUES ('Semerkant', 'Taksim', 6.5),
                           ('Cati', 'Resitpasa', 6.0),
                           ('Beat', 'Taksim', 8.0)"""
        cursor.execute(query)

        connection.commit()
    return redirect(url_for('home_page'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count

@app.route('/culture')
def culture_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """SELECT * FROM Culture"""
        cursor.execute(query)
        culture_data = json.dumps(cursor.fetchall())
        culture = json.loads(culture_data)

    now = datetime.datetime.now()
    return render_template('culture.html', current_time=now.ctime(), culture=culture)

@app.route('/entertainment')
def entertainment_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """SELECT * FROM Entertainment"""
        cursor.execute(query)
        entertainment_data = json.dumps(cursor.fetchall())
        entertainment = json.loads(entertainment_data)
    now = datetime.datetime.now()
    return render_template('entertainment.html', current_time=now.ctime(), entertainment = entertainment)

@app.route('/landmark')
def landmark_page():
    now = datetime.datetime.now()
    return render_template('landmark.html', current_time=now.ctime())

@app.route('/caferest')
def caferest_page():
    now = datetime.datetime.now()
    return render_template('caferest.html', current_time=now.ctime())

@app.route('/agency')
def agency_page():
    now = datetime.datetime.now()
    return render_template('agency.html', current_time=now.ctime())

if __name__ == '__main__':

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
