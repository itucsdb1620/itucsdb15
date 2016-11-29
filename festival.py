from settings import *
from cities import *

@app.route('/festival')
def festival_page():
    statement_fest = """SELECT Festival.ID, Festival.NAME, CITY_ID, CATEGORY, SCORE, Cities.Name FROM Festival
                        LEFT OUTER JOIN Cities ON (Festival.CITY_ID = Cities.ID)"""
    statement_cities = """SELECT ID,NAME FROM Cities"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement_fest)
            fest_data = json.dumps(cursor.fetchall())
            festival = json.loads(fest_data)

            cursor.execute(statement_cities)
            cities_data = json.dumps(cursor.fetchall())
            cities = json.loads(cities_data)

    now = datetime.datetime.now()
    return render_template('festival.html', current_time=now.ctime(), festival=festival, cities=cities)


@app.route('/festival/<int:id>')
def festival_update_page(id):
    statement_fest = """SELECT Festival.ID, Festival.NAME, CITY_ID, CATEGORY, SCORE, Cities.Name FROM Festival
                        LEFT OUTER JOIN Cities ON (Festival.CITY_ID = Cities.ID) WHERE (Festival.ID = %s)"""
    statement_cities = """SELECT ID,NAME FROM Cities"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement_fest, (id,))
            fest_data = json.dumps(cursor.fetchall())
            festival = json.loads(fest_data)

            cursor.execute(statement_cities)
            cities_data = json.dumps(cursor.fetchall())
            cities = json.loads(cities_data)

    return render_template('festival_update.html', festival=festival, cities=cities)


@app.route('/festival/delete_all')
def delete_all_festival():
    statement = """DELETE FROM Festival"""

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)

    return redirect(url_for('festival_page'))


@app.route('/festival/insert', methods=["POST"])
def insert_festival():
    statement = "INSERT INTO Festival (NAME, CITY_ID, CATEGORY, SCORE) VALUES (%s, %s, %s, %s)"
    name = request.form['name']
    city = request.form['city']
    category = request.form['category']
    score = request.form['score']

    with dbapi2.connect(app.config['dsn']) as connection:
         with connection.cursor() as cursor:
            cursor.execute(statement, (name, city, category, score))

    return redirect(url_for('festival_page'))


@app.route('/festival/delete', methods=["POST"])
def delete_festival():
    statement = """DELETE FROM Festival WHERE ID = %s"""
    ids = request.form.getlist("festivals_to_delete")

    for id in ids:
        with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                cursor.execute(statement, (id))

    return redirect(url_for('festival_page'))


@app.route('/festival/update', methods=["POST"])
def update_festival():
    id = request.form["festival_index"]
    name = request.form["update_festival_name"]
    city = request.form["update_festival_city"]
    category = request.form["update_festival_category"]
    score = request.form["update_festival_score"]

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Festival SET NAME = %s WHERE ID = %s"""
                cursor.execute(statement, (name, id))
            if city:
                statement = """UPDATE Festival SET CITY_ID = %s WHERE ID = %s"""
                cursor.execute(statement, (city, id))
            if category:
                statement = """UPDATE Festival SET CATEGORY = %s WHERE ID = %s"""
                cursor.execute(statement, (category, id))
            if score:
                statement = """UPDATE CafeRest SET SCORE = %s WHERE ID = %s"""
                cursor.execute(statement, (score, id))

    return redirect(url_for('festival_page'))
