from settings import *

@app.route('/users')
def users_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT PEOPLE.ID, PEOPLE.NAME, PEOPLE.SURNAME,
                        PEOPLE.USERNAME, PEOPLE.EMAIL, PEOPLE.AGE, PEOPLE.PHOTO,
                        PEOPLE.WHENCE_ID, Cities.NAME FROM PEOPLE
                        LEFT OUTER JOIN Cities
                        ON PEOPLE.WHENCE_ID=Cities.ID """
            cursor.execute(query)
            people_data = json.dumps(cursor.fetchall())
            people = json.loads(people_data)
                    ##########################################################

    now = datetime.datetime.now()
    return render_template('users.html', current_time=now.ctime(), people=people)
