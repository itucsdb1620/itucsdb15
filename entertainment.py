from settings import *

@app.route('/entertainment')
def entertainment_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM Entertainment"""
            cursor.execute(query)
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)

    now = datetime.datetime.now()
    return render_template('entertainment.html', current_time=now.ctime(), entertainment=entertainment)

@app.route('/entertainment/details', methods =["POST"])
def entertainment_details():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Entertainment WHERE (ID = %s)"""
            cursor.execute(statement, (id))
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)
    return render_template('entertainment_details.html', entertainment = entertainment)

@app.route('/entertainment/insert', methods=["POST"])
def entertainment_insert():
    name = request.form['entertainment_place_name']
    place = request.form['entertainment_place_place']
    score = request.form['entertainment_place_score']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """INSERT INTO Entertainment (NAME, PLACE, SCORE)
                        VALUES (%s, %s, %s)"""
            cursor.execute(statement, (name,place,score))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/delete', methods=["POST"])
def entertainment_delete():
    ID = request.form['entertainment_place_ID']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Entertainment
                        WHERE (ID = %s)"""
            cursor.execute(statement, (ID))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/update', methods=["POST"])
def entertainment_update():
    id = request.form['entertainment_index']
    name = request.form['entertainment_update_name']
    place = request.form['entertainment_update_place']
    score = request.form['entertainment_update_score']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Entertainment
                            SET (NAME) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if place:
                statement = """UPDATE Entertainment
                            SET (PLACE) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (place,id))
            if score:
                statement = """UPDATE Entertainment
                            SET (SCORE) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (score,id))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/delete_all')
def entertainment_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Entertainment"""
            cursor.execute(query)

    return redirect(url_for('entertainment_page'))