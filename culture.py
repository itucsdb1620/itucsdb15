from settings import *

@app.route('/culture')
def culture_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT Culture.ID, Culture.NAME, Culture.SCORE,
                        Culture.VOTES, Culture.INFO, Culture.PHOTO,
                        Culture.ACTIVITY_ID, Activities.NAME, Countries.Name, Cities.Name
                        FROM Culture
                        LEFT OUTER JOIN Activities
                        ON Culture.ACTIVITY_ID=Activities.ID
                        LEFT OUTER JOIN Cities
                        ON Culture.CITY_ID=Cities.ID
                        LEFT OUTER JOIN Countries
                        ON Cities.COUNTRY=Countries.ID
                        ORDER BY Culture.SCORE DESC"""
            cursor.execute(query)
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)
            for place in culture:
                place[2] = "{:2.2f}".format(place[2])
            query = """SELECT ID,NAME FROM Activities"""
            cursor.execute(query)
            activity_data = json.dumps(cursor.fetchall())
            activities = json.loads(activity_data)

            query = """SELECT ID,NAME FROM Cities"""
            cursor.execute(query)
            city_data = json.dumps(cursor.fetchall())
            cities = json.loads(city_data)

    now = datetime.datetime.now()
    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    return render_template('culture.html', current_time=now.ctime(), culture=culture, activities=activities, cities=cities, usernum=usernum)

@app.route('/culture/<int:id>')
def culture_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT Culture.ID, Culture.NAME, Culture.SCORE,
                        Culture.VOTES, Culture.INFO, Culture.PHOTO,
                        Culture.ACTIVITY_ID, Activities.NAME , Countries.Name, Cities.Name
                        FROM Culture
                        LEFT OUTER JOIN Activities
                        ON Culture.ACTIVITY_ID=Activities.ID
                        LEFT OUTER JOIN Cities
                        ON Culture.CITY_ID=Cities.ID
                        LEFT OUTER JOIN Countries
                        ON Cities.COUNTRY=Countries.ID
                        WHERE (Culture.ID = %s)"""
            cursor.execute(statement, (id,))
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)

            query = """SELECT ID,NAME FROM Activities"""
            cursor.execute(query)
            activity_data = json.dumps(cursor.fetchall())
            activities = json.loads(activity_data)

            query = """SELECT ID,NAME FROM Cities"""
            cursor.execute(query)
            city_data = json.dumps(cursor.fetchall())
            cities = json.loads(city_data)
    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    return render_template('culture_details.html', culture=culture, activities=activities, cities=cities, usernum=usernum)

@app.route('/culture/insert', methods=["POST"])
def culture_insert():
    name = request.form['cultural_place_name']
    score = request.form['cultural_place_score']
    votes = request.form['cultural_place_votes']
    info = request.form['cultural_place_info']
    photo = request.form['cultural_place_photo']
    activity = request.form['cultural_activity_id']
    city = request.form['cultural_place_city']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and score and votes and activity:
                query = """SELECT * FROM Activities WHERE (ID = %s)"""
                cursor.execute(query, (activity,))
                exists_data = json.dumps(cursor.fetchall())
                exists = json.loads(exists_data)
                if(exists):
                    statement = """INSERT INTO Culture (NAME, SCORE, VOTES, INFO, PHOTO, ACTIVITY_ID, CITY_ID)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(statement, (name,score,votes,info,photo,activity,city))

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
    info = request.form["cultural_info_update"]
    activity = request.form["culture_activity_update"]
    city = request.form['cultural_city_update']
    id = request.form["cultural_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Culture SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                statement = """UPDATE Culture SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if info:
                statement = """UPDATE Culture SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if activity:
                statement = """UPDATE Culture SET ACTIVITY_ID = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (activity,id))
            if city:
                statement = """UPDATE Culture SET CITY_ID = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (city,id))
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