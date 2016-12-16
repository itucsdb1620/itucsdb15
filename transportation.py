from settings import *

@app.route('/transportation')
def transportation_page():
    #if g.user:
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT Transportation.ID, Transportation.NAME, Transportation.INFO, Transportation.PHOTO,
                        Transportation.PLACE, Location.NAME FROM Transportation
                        LEFT OUTER JOIN Location
                        ON Transportation.PLACE=Location.ID"""
            cursor.execute(query)
            transportation_data = json.dumps(cursor.fetchall())
            transportation = json.loads(transportation_data)
            
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
    return render_template('transportation.html', current_time=now.ctime(), transportation=transportation, location=location, usernum=usernum)
    #return redirect(url_for('login_page'))
    
@app.route('/transportation/<int:id>')
def transportation_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT Transportation.ID, Transportation.NAME, Transportation.INFO, Transportation.PHOTO,
                        Transportation.PLACE, Location.NAME FROM Transportation
                        LEFT OUTER JOIN Location
                        ON Transportation.PLACE=Location.ID
                        WHERE (Transportation.ID = %s)"""
            cursor.execute(statement, (id,))
            transportation_data = json.dumps(cursor.fetchall())
            transportation = json.loads(transportation_data)
            
            query = """SELECT ID,NAME FROM Location"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)

    return render_template('transportation_details.html', transportation=transportation, location=location)

@app.route('/transportation/insert', methods=["POST"])
def transportation_insert():
    name = request.form['transportation_place_name']
    info = request.form['transportation_place_info']
    photo = request.form['transportation_place_photo']
    place = request.form['transportation_place']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and place:
                query = """SELECT * FROM Location WHERE (ID = %s)"""
                cursor.execute(query, (place,))
                exists_data = json.dumps(cursor.fetchall())
                exists = json.loads(exists_data)
                if(exists):
                    if photo:
                        statement = """INSERT INTO Entertainment (NAME, INFO, PHOTO, PLACE)
                            VALUES (%s, %s, %s, %s)"""
                        cursor.execute(statement, (name,info,photo,place))
                    else:
                        statement = """INSERT INTO Entertainment (NAME, INFO, PLACE)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
                        cursor.execute(statement, (name,info,place))        
    return redirect(url_for('transportation_page'))

@app.route('/transportation/delete', methods=["POST"])
def transportation_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Transportation
                        WHERE (ID = %s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('transportation_page'))

@app.route('/transportation/update', methods=["POST"])
def transportation_update():
    id = request.form['transportation_index']
    name = request.form['transportation_update_name']
    photo = request.form["transportation_update_photo"]
    info = request.form["transportation_update_info"]
    place = request.form['transportation_update_place']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Transportation
                            SET (NAME) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if info:
                statement = """UPDATE Transportation
                            SET (INFO) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if photo:
                statement = """UPDATE Transportation
                            SET (PHOTO) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if place:
                statement = """UPDATE Transportation
                            SET (PLACE) = (%s)
                            WHERE (ID = %s)"""
                cursor.execute(statement, (place,id))

    return redirect(url_for('transportation_page'))

@app.route('/transportation/delete_all')
def transportation_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Transportation"""
            cursor.execute(query)

    return redirect(url_for('transportation_page'))
