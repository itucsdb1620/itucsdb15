from settings import *

@app.route('/entertainment')
def entertainment_page():
    #if g.user:
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT Entertainment.ID, Entertainment.NAME, Entertainment.SCORE,
                        Entertainment.VOTES, Entertainment.INFO, Entertainment.PHOTO,
                        Entertainment.ACTIVITY, Entertainment.PLACE, Activities.NAME, Location.NAME FROM Entertainment
                        LEFT OUTER JOIN Location
                        ON Entertainment.PLACE=Location.ID
                        LEFT OUTER JOIN Activities
                        ON Entertainment.ACTIVITY=Activities.ID"""
            cursor.execute(query)
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)
            
            for place in entertainment:
                place[2] = "{:2.2f}".format(place[2])

            query = """SELECT ID,NAME FROM Activities"""
            cursor.execute(query)
            activity_data = json.dumps(cursor.fetchall())
            activities = json.loads(activity_data)
            
            query = """SELECT ID,NAME FROM Location"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)

    now = datetime.datetime.now()
    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    return render_template('entertainment.html', current_time=now.ctime(), entertainment=entertainment, activities=activities, location=location, usernum=usernum)
    #return redirect(url_for('login_page'))
    
@app.route('/entertainment/<int:id>')
def entertainment_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT Entertainment.ID, Entertainment.NAME, Entertainment.SCORE,
                        Entertainment.VOTES, Entertainment.INFO, Entertainment.PHOTO,
                        Entertainment.ACTIVITY, Entertainment.PLACE, Activities.NAME, Location.NAME FROM Entertainment
                        LEFT OUTER JOIN Location
                        ON Entertainment.PLACE=Location.ID
                        LEFT OUTER JOIN Activities
                        ON Entertainment.ACTIVITY=Activities.ID WHERE (Entertainment.ID = %s)"""
            cursor.execute(statement, (id,))
            entertainment_data = json.dumps(cursor.fetchall())
            entertainment = json.loads(entertainment_data)

            query = """SELECT ID,NAME FROM Activities"""
            cursor.execute(query)
            activities_data = json.dumps(cursor.fetchall())
            activities = json.loads(activities_data)
            
            query = """SELECT ID,NAME FROM Location"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)

    return render_template('entertainment_details.html', entertainment=entertainment, activities=activities, location=location)

@app.route('/entertainment/insert', methods=["POST"])
def entertainment_insert():
    name = request.form['entertainment_place_name']
    score = request.form['entertainment_place_score']
    votes = request.form['entertainment_place_votes']
    info = request.form['entertainment_place_info']
    photo = request.form['entertainment_place_photo']
    activity = request.form['entertainment_activity']
    place = request.form['entertainment_place']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and score and votes and place and activity:
                query = """SELECT * FROM Location WHERE (ID = %s)"""
                cursor.execute(query, (place,))
                exists1_data = json.dumps(cursor.fetchall())
                exists1 = json.loads(exists1_data)
                query = """SELECT * FROM Activities WHERE (ID = %s)"""
                cursor.execute(query, (activity,))
                exists2_data = json.dumps(cursor.fetchall())
                exists2 = json.loads(exists2_data)
                if(exists1 and exists2):
                    if photo:
                        statement = """INSERT INTO Entertainment (NAME, SCORE, VOTES, INFO, PHOTO, ACTIVITY, PLACE)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                        cursor.execute(statement, (name,score,votes,info,photo,activity,place))
                    else:
                        statement = """INSERT INTO Entertainment (NAME, SCORE, VOTES, INFO, ACTIVITY, PLACE)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                        cursor.execute(statement, (name,score,votes,info,activity,place))        
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
    activity = request.form['entertainment_update_activity']
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
            if activity:
                statement = """UPDATE Entertainment
                            SET (ACTIVITY) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (activity,id))
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

    return redirect(url_for('entertainment_details', id=id))
