from settings import *

@app.route('/people/<int:id>')
def people_page(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT PEOPLE.ID, PEOPLE.NAME, PEOPLE.SURNAME,
                        PEOPLE.USERNAME, PEOPLE.EMAIL, PEOPLE.AGE, PEOPLE.PHOTO,
                        PEOPLE.WHENCE_ID, Cities.NAME FROM PEOPLE
                        LEFT OUTER JOIN Cities
                        ON PEOPLE.WHENCE_ID=Cities.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            people_data = json.dumps(cursor.fetchall())
            people = json.loads(people_data)
                    ##########################################################

            query = """SELECT Activities.NAME, Activities.INFO FROM PEOPLE
                        LEFT OUTER JOIN Activities
                        ON PEOPLE.BEST_ACTIVITY_ID=Activities.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            activity_data = json.dumps(cursor.fetchall())
            activity = json.loads(activity_data)

            query = """SELECT ID, NAME FROM Cities"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)
                     ##########################################################

            query = """SELECT Location.NAME, Location.INFO, Location.Photo FROM PEOPLE
                        LEFT OUTER JOIN Location
                        ON PEOPLE.BEST_PLACE_ID=Location.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            place_data = json.dumps(cursor.fetchall())
            place = json.loads(place_data)
                    ##########################################################

            query = """SELECT Culture.NAME, Culture.INFO, Culture.Photo FROM PEOPLE
                        LEFT OUTER JOIN Culture
                        ON PEOPLE.BEST_CULTURE_ID=Culture.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)
                    ##########################################################


    now = datetime.datetime.now()
    return render_template('people.html', people=people, location=location, activity=activity, place=place, culture=culture)

#@app.route('/people/<int:id>')
#def people_details(id):
#    with dbapi2.connect(app.config['dsn']) as connection:
#        with connection.cursor() as cursor:
#            statement = """SELECT NAME, SURNAME FROM PEOPLE WHERE (ID = %s)"""
#            cursor.execute(statement, (id,))
#            people_data = json.dumps(cursor.fetchall())
#            people = json.loads(people_data)
#        return render_template('people.html')

@app.route('/people/insert', methods=["POST"])
def people_insert():
    surname = request.form['surname']
    name = request.form['name']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """INSERT INTO PEOPLE (NAME, SURNAME)
                        VALUES (%s,%s )"""
                cursor.execute(statement, (name,surname ))

    return redirect(url_for('people_page'))

@app.route('/people/delete', methods=["POST"])
def people_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM PEOPLE WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('people_page'))

@app.route('/people/update', methods=["POST"])
def people_update():
    name = request.form["name_update"]
    surname = request.form["surname_update"]
    id = request.form["people_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE PEOPLE SET NAME = (%s) WHERE (NAME = %s)"""
                cursor.execute(statement, (name,id))
            if surname:
                statement = """UPDATE PEOPLE SET SURNAME = (%s) WHERE (NAME = %s)"""
                cursor.execute(statement, (surname,id))

    return redirect(url_for('people_page',))

@app.route('/people/delete_all')
def people_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM PEOPLE"""
            cursor.execute(query)

    return redirect(url_for('people_page'))



