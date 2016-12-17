from settings import *

@app.route('/landmark')
def landmark_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT LANDMARK.ID, LANDMARK.NAME, LANDMARK.SCORE,
                        LANDMARK.INFO, LANDMARK.LOCATIONID, Cities.NAME, LANDMARK.PHOTO FROM LANDMARK
                        LEFT OUTER JOIN Cities
                        ON LANDMARK.LOCATIONID=Cities.ID
                        ORDER BY LANDMARK.SCORE DESC"""
            cursor.execute(query)
            landmark_data = json.dumps(cursor.fetchall())
            landmark = json.loads(landmark_data)
            for score in landmark:
                score[2] = "{:2.2f}".format(score[2])

            query = """SELECT ID, NAME FROM Cities"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            locations = json.loads(location_data)

    now = datetime.datetime.now()

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2

    return render_template('landmark.html', current_time=now.ctime(), landmark=landmark, locations=locations, usernum=usernum)

@app.route('/landmark/<int:id>')
def landmark_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT LANDMARK.ID, LANDMARK.NAME, LANDMARK.SCORE,
                        LANDMARK.INFO, LANDMARK.LOCATIONID, Cities.NAME, LANDMARK.PHOTO FROM LANDMARK
                        LEFT OUTER JOIN Cities
                        ON LANDMARK.LOCATIONID=Cities.ID WHERE (LANDMARK.ID = %s)"""
            cursor.execute(statement, (id,))
            landmark_data = json.dumps(cursor.fetchall())
            landmark = json.loads(landmark_data)

            query = """SELECT ID, NAME FROM Cities"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            locations = json.loads(location_data)

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2

    return render_template('landmark_details.html', landmark=landmark, locations=locations, usernum=usernum)

@app.route('/landmark/insert', methods=["POST"])
def landmark_insert():
    name = request.form['landmark_name']
    score = request.form['landmark_score']
    info = request.form['landmark_info']
    location = request.form['location_id']
    photo =  request.form['landmark_photo']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and score and location:
                query = """SELECT * FROM Cities WHERE (ID = %s)"""
                cursor.execute(query, (location,))
                exists_data = json.dumps(cursor.fetchall())
                exists = json.loads(exists_data)
                if(exists):
                    statement = """INSERT INTO LANDMARK (NAME, SCORE, INFO, LOCATIONID, PHOTO)
                        VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(statement, (name,score,info,location,photo))

    return redirect(url_for('landmark_page'))

@app.route('/landmark/delete', methods=["POST"])
def landmark_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM LANDMARK WHERE ID = (%s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('landmark_page'))

@app.route('/landmark/update', methods=["POST"])
def landmark_update():
    name = request.form["name_update"]
    score = request.form["score_update"]
    info = request.form["info_update"]
    city = request.form["city_update"]
    id = request.form["landmark_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE LANDMARK SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if info:
                statement = """UPDATE LANDMARK SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if city:
                statement = """UPDATE LANDMARK SET LOCATIONID = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (city,id))
            if score:
                statement = """UPDATE LANDMARK SET SCORE = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (score,id))
    return redirect(url_for('landmark_page'))

@app.route('/landmark/delete_all')
def landmark_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM LANDMARK"""
            cursor.execute(query)

    return redirect(url_for('landmark_page'))

@app.route('/landmark/vote', methods=['POST'])
def landmark_vote():
    vote = request.form["vote"]
    id = request.form["landmark_vote_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if vote:
                statement = """UPDATE LANDMARK SET SCORE = (SCORE * VOTES + %s) / (VOTES+1),
                            VOTES = VOTES + 1 WHERE (ID = %s)"""
                cursor.execute(statement, (vote,id))

    return redirect(url_for('landmark_details', id=id))

