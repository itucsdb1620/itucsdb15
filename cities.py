from settings import *

@app.route('/cities')
def cities_page():
    statement = """SELECT * FROM Cities"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            cities_data = json.dumps(cursor.fetchall())
            cities = json.loads(cities_data)

    now = datetime.datetime.now()
    return render_template('cities.html', current_time=now.ctime(), cities=cities)


@app.route('/cities/<int:id>')
def cities_update_page(id):
    statement = """SELECT * FROM Cities WHERE ID = %s"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement, (id,))
            cities_data = json.dumps(cursor.fetchall())
            cities = json.loads(cities_data)

    return render_template('cities_update.html', cities=cities)


@app.route('/cities/delete_all')
def delete_all_cities():
    statement = """DELETE FROM Cities"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)

    return redirect(url_for('cities_page'))


@app.route('/cities/insert', methods=["POST"])
def insert_city():
    statement = "INSERT INTO Cities (NAME, COUNTRY) VALUES (%s, %s)"
    name = request.form['name']
    country = request.form['country']

    with dbapi2.connect(app.config['dsn']) as connection:
         with connection.cursor() as cursor:
                cursor.execute(statement, (name, country))

    return redirect(url_for('cities_page'))


@app.route('/cities/delete', methods=["POST"])
def delete_cities():
    statement = """DELETE FROM Cities WHERE ID = %s"""
    ids = request.form.getlist("city_to_delete")

    for id in ids:
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, (id))

    return redirect(url_for('cities_page'))


@app.route('/cities/update', methods=["POST"])
def update_cities():
    id = request.form["cities_index"]
    name = request.form["update_city_name"]
    country = request.form["update_city_country"]

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Cities SET NAME = %s WHERE ID = %s"""
                cursor.execute(statement, (name, id))
            if country:
                statement = """UPDATE Cities SET COUNTRY = %s WHERE ID = %s"""
                cursor.execute(statement, (country, id))

    return redirect(url_for('cities_page'))
