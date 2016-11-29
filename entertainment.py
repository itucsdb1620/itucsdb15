from settings import *

@app.route('/entertainment')
def entertainment_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT Entertainment.ID, Entertainment.NAME, Entertainment.SCORE,
                        Entertainment.VOTES, Entertainment.INFO, Entertainment.PHOTO,
                        Entertainment.PLACE, Places.NAME FROM Entertainment
                        LEFT OUTER JOIN Places
                        ON Entertainment.PLACE=Places.ID"""
            cursor.execute(query)
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)

            query = """SELECT ID,NAME FROM Places"""
            cursor.execute(query)
            place_data = json.dumps(cursor.fetchall())
            places = json.loads(place_data)

    now = datetime.datetime.now()
    return render_template('entertainment.html', current_time=now.ctime(), entertainment=entertainment, places=places)

@app.route('/entertainment/<int:id>')
def entertainment_place(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT Entertainment.ID, Entertainment.NAME, Entertainment.SCORE,
                        Entertainment.VOTES, Entertainment.INFO, Entertainment.PHOTO,
                        Entertainment.PLACE, Places.NAME FROM Entertainment
                        LEFT OUTER JOIN Places
                        ON Entertainment.PLACE=Places.ID WHERE (Entertainment.ID = %s)"""
            cursor.execute(statement, (id,))
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)

            query = """SELECT ID,NAME FROM Places"""
            cursor.execute(query)
            place_data = json.dumps(cursor.fetchall())
            places = json.loads(place_data)

    return render_template('entertainment_place.html', entertainment=entertainment, places = places)

@app.route('/entertainment/details', methods =["POST"])
def entertainment_details():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Entertainment WHERE (ID = %s)"""
            cursor.execute(statement, (id))
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)
    return render_template('entertainment_details.html', entertainment = entertainment)

@app.route('/entertainment/insert', methods=["POST"])
def entertainment_insert():
    name = request.form['entertainment_place_name']
    score = request.form['entertainment_place_score']
    votes = request.form['entertainment_place_votes']
    info = request.form['entertainment_place_info']
    photo = request.form['entertainment_place_photo']
    place = request.form['entertainment_place']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and score and votes and place:
                query = """SELECT * FROM Places WHERE (ID = %s)"""
                cursor.execute(query, (place,))
                exists_data = json.dumps(cursor.fetchall())
                exists = json.loads(exists_data)
                if(exists):
                    statement = """INSERT INTO Entertainment (NAME, SCORE, VOTES, INFO, PHOTO, PLACE)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(statement, (name,score,votes,info,photo,place))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/delete', methods=["POST"])
def entertainment_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Entertainment
                        WHERE (ID = %s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/update', methods=["POST"])
def entertainment_update():
    id = request.form['entertainment_index']
    name = request.form['entertainment_update_name']
    photo = request.form["entertainment_update_photo"]
    info = request.form["entertainment_update_info"]
    place = request.form['entertainment_update_place']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Entertainment
                            SET (NAME) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if info:
                statement = """UPDATE Entertainment
                            SET (INFO) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if photo:
                statement = """UPDATE Entertainment
                            SET (PHOTO) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if place:
                statement = """UPDATE Entertainment
                            SET (PLACE) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (place,id))

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/delete_all')
def entertainment_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Entertainment"""
            cursor.execute(query)

    return redirect(url_for('entertainment_page'))

@app.route('/entertainment/vote', methods=['POST'])
def entertainment_voting():
    vote = request.form["vote"]
    id = request.form["entertainment_index2"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if vote:
                statement = """UPDATE Entertainment SET SCORE = (SCORE * VOTES + %s) / (VOTES+1),
                            VOTES = VOTES + 1 WHERE (ID = %s)"""
                cursor.execute(statement, (vote,id))

    return redirect(url_for('entertainment_place', id=id))
