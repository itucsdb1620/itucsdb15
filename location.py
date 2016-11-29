from settings import *

@app.route('/location')
def location_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM LOCATION"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)

    now = datetime.datetime.now()
    return render_template('location.html', current_time=now.ctime(), location=location)

@app.route('/location/<int:id>')
def location_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT CITYNAME FROM LOCATION WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)
    return render_template('landmark.html')

@app.route('/location/insert', methods=["POST"])
def location_insert():
    city = request.form['city_name']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if city:
                statement = """INSERT INTO LOCATION (CITYNAME)
                        VALUES (%s )"""
                cursor.execute(statement, (city, ))

    return redirect(url_for('location_page'))

@app.route('/location/delete', methods=["POST"])
def location_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM LOCATION WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('location_page'))

@app.route('/location/update', methods=["POST"])
def location_update():
    city = request.form["city_update"]
    id = request.form["location_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if city:
                statement = """UPDATE LOCATION SET CITYNAME = (%s) WHERE (CITYNAME = %s)"""
                cursor.execute(statement, (city,id))

    return redirect(url_for('landmark_page',))

@app.route('/location/delete_all')
def location_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM LOCATION"""
            cursor.execute(query)

    return redirect(url_for('location_page'))



