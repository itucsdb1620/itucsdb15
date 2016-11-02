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

@app.route('/culture/<string:name>')
def culture_details(name):
    return render_template('culture_details.html', name=name)

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

@app.route('/culture/delete')
def culture_delete():
    return redirect(url_for('culture_page'))

@app.route('/culture/update')
def culture_update():
    return redirect(url_for('culture_page'))

@app.route('/culture/delete_all')
def culture_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Culture"""
            cursor.execute(query)

    return redirect(url_for('culture_page'))