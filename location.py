from settings import *
from itertools import count

@app.route('/location')
def location_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT Location.ID, Location.NAME, Location.INFO, Location.PHOTO,
                        Cities.NAME, Countries.NAME FROM Cities JOIN Countries
                        ON Cities.Country = Countries.ID
                        LEFT OUTER JOIN Location
                        ON Location.City=Cities.ID"""
            cursor.execute(statement)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)
    
            query = """SELECT ID,NAME FROM Cities"""
            cursor.execute(query)
            city_data = json.dumps(cursor.fetchall())
            city = json.loads(city_data)
            
            query = """SELECT ID,NAME FROM Countries"""
            cursor.execute(query)
            country_data = json.dumps(cursor.fetchall())
            country = json.loads(country_data)
    now = datetime.datetime.now()
    return render_template('location.html', current_time=now.ctime(), location=location, city = city, country = country)

@app.route('/location/<int:id>')
def location_details(id):
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """SELECT * FROM Location WHERE (ID = %s)"""
            cursor.execute(statement, (id,))
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)
            
            query = """SELECT ID,NAME FROM Cities"""
            cursor.execute(query)
            city_data = json.dumps(cursor.fetchall())
            city = json.loads(city_data)
            
            query = """SELECT ID,NAME FROM Countries"""
            cursor.execute(query)
            country_data = json.dumps(cursor.fetchall())
            country = json.loads(country_data)
            
    return render_template('location_details.html', location=location, city = city, country = country)

@app.route('/location/insert', methods=["POST"])
def location_insert():
    name = request.form['location_name']
    info = request.form['location_info']
    photo = request.form['location_photo']
    city = request.form['location_city']
    country = request.form['location_country']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                if photo:
                    statement = """INSERT INTO Location (NAME, INFO, PHOTO, CITY, COUNTRY)
                        VALUES (%s, %s, %s, %s)"""
                    cursor.execute(statement, (name,info,photo,city,country)) 
                else: 
                    statement = """INSERT INTO Location (NAME, INFO, CITY, COUNTRY)
                            VALUES (%s, %s, %s, %s)"""
                    cursor.execute(statement, (name,info,city,country))
    return redirect(url_for('location_page'))

@app.route('/location/delete', methods=["POST"])
def location_delete():
    id = request.form["select"]
    id = int(id)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """DELETE FROM Location WHERE ID = (%s)"""
            cursor.execute(statement, (id,))

    return redirect(url_for('location_page'))

@app.route('/location/update', methods=["POST"])
def location_update():
    name = request.form['location_update_name']
    photo = request.form['location_update_photo']
    info = request.form['location_update_info']
    city = request.form['location_update_city']
    country = request.form['location_update_country']
    id = request.form['location_index']
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            if name:
                statement = """UPDATE Location SET (NAME) = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (name,id))
            if photo:
                statement = """UPDATE Location SET PHOTO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (photo,id))
            if info:
                statement = """UPDATE Location SET INFO = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (info,id))
            if city:
                statement = """UPDATE Location SET CITY = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (city,id))
            if country:
                statement = """UPDATE Location SET COUNTRY = (%s) WHERE (ID = %s)"""
                cursor.execute(statement, (country,id))
    return redirect(url_for('location_details',id=id))

@app.route('/location/delete_all')
def location_delete_all():
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            query = """DELETE FROM Location"""
            cursor.execute(query)

    return redirect(url_for('location_page'))




