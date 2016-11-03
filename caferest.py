from settings import *

@app.route('/caferest')
def caferest_page():
    query = """SELECT * FROM CafeRest ORDER BY ID"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            caferest_data = json.dumps(cursor.fetchall())
            caferest = json.loads(caferest_data)

    now = datetime.datetime.now()
    return render_template('caferest.html', current_time=now.ctime(), caferest=caferest)


@app.route('/caferest/<int:id>')
def caferest_update_page(id):
    statement = """SELECT * FROM CafeRest WHERE ID = %s"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement, (id,))
            caferest_data = json.dumps(cursor.fetchall())
            caferest = json.loads(caferest_data)

    return render_template('caferest_update.html', caferest=caferest)


@app.route('/caferest/delete_all')
def delete_all_caferest():
    statement = """DELETE FROM CafeRest"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)

    return redirect(url_for('caferest_page'))


@app.route('/caferest/insert', methods=["POST"])
def insert_caferest():
    statement = "INSERT INTO CafeRest (NAME, CITY, CUISINE, SCORE) VALUES (%s, %s, %s, %s)"
    name = request.form['name']
    city = request.form['city']
    cuisine = request.form['cuisine']
    score = request.form['score']

    with dbapi2.connect(app.config['dsn']) as connection:
         with connection.cursor() as cursor:
                cursor.execute(statement, (name, city, cuisine, score))

    return redirect(url_for('caferest_page'))


@app.route('/caferest/delete', methods=["POST"])
def delete_caferest():
    statement = """DELETE FROM CafeRest WHERE ID = %s"""
    ids = request.form.getlist("cafes_to_delete")

    for id in ids:
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, (id))

    return redirect(url_for('caferest_page'))


@app.route('/caferest/update', methods=["POST"])
def update_caferest():
    id = request.form["caferest_index"]
    name = request.form["update_caferest_name"]
    city = request.form["update_caferest_city"]
    cuisine = request.form["update_caferest_cuisine"]
    score = request.form["update_caferest_score"]

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE CafeRest SET NAME = %s WHERE ID = %s"""
                cursor.execute(statement, (name, id))
            if city:
                statement = """UPDATE CafeRest SET CITY = %s WHERE ID = %s"""
                cursor.execute(statement, (city, id))
            if cuisine:
                statement = """UPDATE CafeRest SET CUISINE = %s WHERE ID = %s"""
                cursor.execute(statement, (cuisine, id))
            if score:
                statement = """UPDATE CafeRest SET SCORE = %s WHERE ID = %s"""
                cursor.execute(statement, (score, id))

    return redirect(url_for('caferest_page'))
