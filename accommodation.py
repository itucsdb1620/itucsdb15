from settings import *

@app.route('/accommodation')
def accommodation_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM Accommodation ORDER BY SCORE DESC"""
            cursor.execute(query)
            places_data = json.dumps(cursor.fetchall())
            places = json.loads(places_data)
            for place in places:
                place[2] = "{:2.2f}".format(place[2])

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    now = datetime.datetime.now()
    return render_template('accommodation.html', current_time=now.ctime(), places=places, usernum=usernum)

@app.route('/accommodation/<int:id>')
def accommodation_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Accommodation WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            places_data = json.dumps(cursor.fetchall())
            places = json.loads(places_data)
    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    return render_template('accommodation_details.html', places=places, usernum=usernum)

@app.route('/accommodation/insert', methods=["POST"])
def accommodation_insert():
    name = request.form['accommodation_name']
    score = request.form['accommodation_place_score']
    votes = request.form['accommodation_place_votes']
    info = request.form['accommodation_info']
    photo = request.form['accommodation_photo']
    type = request.form['accommodation_type']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """INSERT INTO Accommodation (NAME, INFO, SCORE, VOTES, PHOTO, TYPE)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(statement, (name,info,score,votes,photo,type))

    return redirect(url_for('accommodation_page'))

@app.route('/accommodation/delete', methods=["POST"])
def accommodation_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Accommodation WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('accommodation_page'))

@app.route('/accommodation/update', methods=["POST"])
def accommodation_update():
    name = request.form["accommodation_name_update"]
    photo = request.form["accommodation_photo_update"]
    info = request.form["accommodation_info_update"]
    type = request.form["accommodation_type_update"]
    id = request.form["accommodation_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Accommodation SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                statement = """UPDATE Accommodation SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if info:
                statement = """UPDATE Accommodation SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if type:
                statement = """UPDATE Accommodation SET TYPE = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (type,id))
    return redirect(url_for('accommodation_details',id=id))

@app.route('/accommodation/delete_all')
def accommodation_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Accommodation"""
            cursor.execute(query)

    return redirect(url_for('accommodation_page'))

@app.route('/accommodation/vote', methods=['POST'])
def accommodation_voting():
    vote = request.form["vote"]
    id = request.form["accommodation_index2"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if vote:
                statement = """UPDATE Accommodation SET SCORE = (SCORE * VOTES + %s) / (VOTES+1),
                            VOTES = VOTES + 1 WHERE (ID = %s)"""
                cursor.execute(statement, (vote,id))

    return redirect(url_for('accommodation_details', id=id))



