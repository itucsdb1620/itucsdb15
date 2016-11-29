from settings import *

@app.route('/places')
def places_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM Places"""
            cursor.execute(query)
            place_data = json.dumps(cursor.fetchall())
            places = json.loads(place_data)

    now = datetime.datetime.now()
    return render_template('places.html', current_time=now.ctime(), places=places)

@app.route('/places/<int:id>')
def places_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Places WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            place_data = json.dumps(cursor.fetchall())
            places = json.loads(place_data)
    return render_template('places_details.html', places=places)

@app.route('/places/insert', methods=["POST"])
def places_insert():
    name = request.form['places_name']
    info = request.form['places_info']
    photo = request.form['places_photo']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """INSERT INTO Places (NAME, INFO, PHOTO)
                        VALUES (%s, %s, %s)"""
                cursor.execute(statement, (name,info,photo))

    return redirect(url_for('places_page'))

@app.route('/places/delete', methods=["POST"])
def places_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Places WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('places_page'))

@app.route('/places/update', methods=["POST"])
def places_update():
    name = request.form['places_update_name']
    photo = request.form['places_update_photo']
    info = request.form['places_update_info']
    id = request.form['place_index']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Places SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                statement = """UPDATE Places SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if info:
                statement = """UPDATE Places SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
    return redirect(url_for('places_details',id=id))

@app.route('/places/delete_all')
def places_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Places"""
            cursor.execute(query)

    return redirect(url_for('places_page'))



