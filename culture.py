from settings import *

@app.route('/culture')
def culture_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM Culture"""
            cursor.execute(query)
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)

    now = datetime.datetime.now()
    return render_template('culture.html', current_time=now.ctime(), culture=culture)

@app.route('/culture/<int:id>')
def culture_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Culture WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)
    return render_template('culture_details.html', culture=culture)

@app.route('/culture/insert', methods=["POST"])
def culture_insert():
    name = request.form['cultural_place_name']
    score = request.form['cultural_place_score']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """INSERT INTO Culture (NAME, SCORE)
                        VALUES (%s, %s)"""
            cursor.execute(statement, (name,score))

    return redirect(url_for('culture_page'))

@app.route('/culture/delete', methods=["POST"])
def culture_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Culture WHERE ID = (%s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('culture_page'))

@app.route('/culture/update', methods=["POST"])
def culture_update():
    name = request.form["cultural_name_update"]
    score = request.form["cultural_score_update"]
    id = request.form["cultural_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Culture SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if score:
                statement = """UPDATE Culture SET (SCORE) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (score,id))
    return redirect(url_for('culture_page'))

@app.route('/culture/delete_all')
def culture_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Culture"""
            cursor.execute(query)

    return redirect(url_for('culture_page'))