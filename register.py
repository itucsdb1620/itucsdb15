from settings import *

@app.route('/registration')
def register_page():
    now = datetime.datetime.now()
    return render_template('register.html', current_time=now.ctime())


@app.route('/registration/register', methods=["POST"])
def register_operation():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['user_name']
    password = request.form['pass']
    repassword = request.form['repass']
    #default photo
    photo ='http://previews.123rf.com/images/richcat/richcat1109/richcat110900082/10732608-Graphic-illustration-of-man-in-business-suit-as-user-icon-avatar-Stock-Vector.jpg'
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and surname and username and (password == repassword):
                statement = """INSERT INTO PEOPLE (NAME, SURNAME, USERNAME, PASSWORD, PHOTO)
                        VALUES (%s,%s,%s,%s,%s )"""
                cursor.execute(statement, (name,surname,username,password,photo ))

            elif (password != repassword):
                ##flash ('Password Conflict') ##
                return redirect(url_for('register_page'))

    return redirect(url_for('new_user_page',username=username))

@app.route('/welcome/<username>')
def new_user_page(username):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT PEOPLE.ID, PEOPLE.NAME, PEOPLE.SURNAME,
                        PEOPLE.USERNAME, PEOPLE.PHOTO FROM PEOPLE
                        WHERE (PEOPLE.USERNAME = %s)"""
            cursor.execute(query,(username, ))
            user_data = json.dumps(cursor.fetchall())
            user = json.loads(user_data)
                    ##########################################################

            query = """SELECT ID, NAME FROM Cities"""
            cursor.execute(query)
            city_data = json.dumps(cursor.fetchall())
            city = json.loads(city_data)

                    ##########################################################
            query = """SELECT ID, NAME FROM Culture"""
            cursor.execute(query)
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)

                    ##########################################################
            query = """SELECT ID, NAME FROM Activities"""
            cursor.execute(query)
            activity_data = json.dumps(cursor.fetchall())
            activity = json.loads(activity_data)

                    ##########################################################

            query = """SELECT ID, NAME FROM Location"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)

    return render_template('new_user.html',user=user, city=city, culture=culture, activity=activity, location=location)

@app.route('/welcome' , methods=["POST"])
def add_info():
    email = request.form['email']
    age = request.form['age']
    age=int(age);
    photo = request.form['photo']
    whence = request.form['whence']
    activity_type = request.form['activity_type']
    activity = request.form['activity']
    district = request.form['district']
    id = request.form['user_index']

    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if email:
                statement = """UPDATE PEOPLE SET (EMAIL) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (email,id ))

            if age:
                statement = """UPDATE PEOPLE SET (AGE) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (age,id  ))

            if photo:
                statement = """UPDATE PEOPLE SET (PHOTO) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id  ))

            if whence:
                statement = """UPDATE PEOPLE SET (WHENCE_ID) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (whence,id  ))

            if activity_type:
                statement = """UPDATE PEOPLE SET (BEST_CULTURE_ID) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (activity_type,id  ))

            if activity:
                statement = """UPDATE PEOPLE SET (BEST_ACTIVITY_ID) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (activity,id  ))

            if district:
                statement = """UPDATE PEOPLE SET (BEST_PLACE_ID) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (district,id  ))

    return redirect(url_for('people_page',id=id))
