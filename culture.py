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
    info = request.form['cultural_place_info']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """INSERT INTO Culture (NAME, SCORE, INFO)
                        VALUES (%s, %s, %s)"""
            cursor.execute(statement, (name,score,info))

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
    photo = request.form["cultural_photo_update"]
    id = request.form["cultural_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Culture SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                 statement = """UPDATE Culture SET PHOTO = (%s) WHERE (ID = %s)"""
                 cursor.execute(statement, (photo,id))
    return redirect(url_for('culture_details',id=id))

@app.route('/culture/delete_all')
def culture_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Culture"""
            cursor.execute(query)

    return redirect(url_for('culture_page'))

@app.route('/culture/vote', methods=['POST'])
def culture_voting():
    vote = request.form["vote"]
    id = request.form["cultural_index2"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if vote:
                statement = """UPDATE Culture SET SCORE = (SCORE * VOTES + %s) / (VOTES+1),
                            VOTES = VOTES + 1 WHERE (ID = %s)"""
                cursor.execute(statement, (vote,id))

    return redirect(url_for('culture_details', id=id))