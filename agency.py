from settings import *

@app.route('/agency')
def agency_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """SELECT * FROM AGENCY
                    ORDER BY SCORE DESC"""
            cursor.execute(query)

            agency_data = json.dumps(cursor.fetchall())
            agency = json.loads(agency_data)
            for score in agency:
                score[2] = "{:2.2f}".format(score[2])

    now = datetime.datetime.now()

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2

    return render_template('agency.html', current_time=now.ctime(), agency=agency, usernum=usernum)

@app.route('/agency/<int:id>')
def agency_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM AGENCY
                        WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            agency_data = json.dumps(cursor.fetchall())
            agency = json.loads(agency_data)

    if g.user:
        if(g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2

    return render_template('agency_details.html', agency=agency, usernum=usernum)

@app.route('/agency/insert', methods=["POST"])
def agency_insert():
    name = request.form['agency_name']
    score = request.form['agency_score']
    info = request.form['agency_info']
    photo =  request.form['agency_photo']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name and score and info and photo:
                    statement = """INSERT INTO AGENCY (NAME, SCORE, INFO, PHOTO)
                        VALUES (%s, %s, %s, %s)"""
                    cursor.execute(statement, (name,score,info,photo))

    return redirect(url_for('agency_page'))

@app.route('/agency/delete', methods=["POST"])
def agency_delete():
    id = request.form["select"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM AGENCY WHERE ID = (%s)"""
            cursor.execute(statement, (id))

    return redirect(url_for('agency_page'))

@app.route('/agency/update', methods=["POST"])
def agency_update():
    name = request.form["name_update"]
    score = request.form["score_update"]
    info = request.form["info_update"]
    photo = request.form["photo_update"]
    id = request.form["agency_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE AGENCY SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if info:
                statement = """UPDATE AGENCY SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if photo:
                statement = """UPDATE AGENCY SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if score:
                statement = """UPDATE AGENCY SET SCORE = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (score,id))
    return redirect(url_for('agency_page'))

@app.route('/agency/delete_all')
def agency_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM AGENCY"""
            cursor.execute(query)

    return redirect(url_for('agency_page'))

@app.route('/agency/vote', methods=['POST'])
def agency_vote():
    vote = request.form["vote"]
    id = request.form["agency_vote_index"]
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if vote:
                statement = """UPDATE AGENCY SET SCORE = (SCORE * VOTES + %s) / (VOTES+1),
                            VOTES = VOTES + 1 WHERE (ID = %s)"""
                cursor.execute(statement, (vote,id))

    return redirect(url_for('agency_details', id=id))
