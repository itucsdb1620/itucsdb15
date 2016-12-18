from settings import *

@app.route('/activities')
def activities_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM Activities"""
            cursor.execute(query)
            activities_data = json.dumps(cursor.fetchall())
            activities = json.loads(activities_data)

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    now = datetime.datetime.now()
    return render_template('activities.html', current_time=now.ctime(), activities=activities, usernum=usernum)

@app.route('/activities/<int:id>')
def activities_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Activities WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            activities_data = json.dumps(cursor.fetchall())
            activities = json.loads(activities_data)
    return render_template('activities_details.html', activities=activities)

@app.route('/activities/insert', methods=["POST"])
def activities_insert():
    name = request.form['activities_name']
    info = request.form['activities_info']
    photo = request.form['activities_photo']
    type = request.form['activities_type']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """INSERT INTO Activities (NAME, INFO, PHOTO, TYPE)
                        VALUES (%s, %s, %s, %s)"""
                cursor.execute(statement, (name,info,photo,type))

    return redirect(url_for('activities_page'))

@app.route('/activities/delete', methods=["POST"])
def activities_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Activities WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('activities_page'))

@app.route('/activities/update', methods=["POST"])
def activities_update():
    name = request.form["activity_name_update"]
    photo = request.form["activity_photo_update"]
    info = request.form["activity_info_update"]
    type = request.form["activity_type_update"]
    id = request.form["activity_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Activities SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                statement = """UPDATE Activities SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if info:
                statement = """UPDATE Activities SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if type:
                statement = """UPDATE Activities SET TYPE = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (type,id))
    return redirect(url_for('activities_details',id=id))

@app.route('/activities/delete_all')
def activities_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Activities"""
            cursor.execute(query)

    return redirect(url_for('activities_page'))



