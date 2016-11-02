from settings import *

@app.route('/landmark')
def landmark_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM LANDMARK"""
            cursor.execute(query)
            landmark_data = json.dumps(cursor.fetchall())
            landmark = json.loads(landmark_data)

    now = datetime.datetime.now()
    return render_template('landmark.html', current_time=now.ctime(), landmark=landmark)

@app.route('/landmark/<int:id>')
def landmark_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM LANDMARK WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            landmark_data = json.dumps(cursor.fetchall())
            landmark = json.loads(landmark_data)
    return render_template('landmark_details.html', landmark=landmark)

@app.route('/landmark/insert', methods=["POST"])
def landmark_insert():
    name = request.form['landmark_name']
    score = request.form['landmark_score']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """INSERT INTO LANDMARK (NAME, SCORE)
                        VALUES (%s, %s)"""
            cursor.execute(statement, (name,score))

    return redirect(url_for('landmark_page'))

@app.route('/landmark/delete', methods=["POST"])
def landmark_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM LANDMARK WHERE ID = (%s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('landmark_page'))

@app.route('/landmark/update', methods=["POST"])
def landmark_update():
    name = request.form["landmark_name_update"]
    score = request.form["landmark_score_update"]
    id = request.form["landmark_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE LANDMARK SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if score:
                statement = """UPDATE LANDMARK SET (SCORE) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (score,id))
    return redirect(url_for('landmark_page'))

@app.route('/landmark/delete_all')
def landmark_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM LANDMARK"""
            cursor.execute(query)

    return redirect(url_for('landmark_page'))