Parts Implemented by Mehmet Tankut Özen
***************************************

1 Database Design
=================

1.1 Database Tables
-------------------

1.1.1 Activities Table
++++++++++++++++++++++

                +---------------+----------------+-----------+-----------+-----------+
                | Name          | Type           | Not Null  |Primary K. |Foreign K. |
                +===============+================+===========+===========+===========+
                | ID            | SERIAL         |   1       |  1        |  0        |
                +---------------+----------------+-----------+-----------+-----------+
                | NAME          | VARCHAR(255)   |   1       |  0        |  0        |
                +---------------+----------------+-----------+-----------+-----------+
                | INFO          | TEXT           |   0       |  0        |  0        |
                +---------------+----------------+-----------+-----------+-----------+
                | PHOTO         | VARCHAR(255)   |   0       |  0        |  0        |
                +---------------+----------------+-----------+-----------+-----------+
                | TYPE          | ACTIVITY_TYPES |   0       |  0        |  0        |
                +---------------+----------------+-----------+-----------+-----------+

.. code-block:: sql
    :linenos:

      CREATE TABLE Activities (
         ID SERIAL PRIMARY KEY,
         NAME VARCHAR(255) NOT NULL,
         INFO TEXT,
         PHOTO VARCHAR(255),
         TYPE ACTIVITY_TYPES
         )

1.1.2 Culture Table
+++++++++++++++++++

                +---------------+--------------+-----------+-----------+-----------+
                | Name          | Type         | Not Null  |Primary K. |Foreign K. |
                +===============+==============+===========+===========+===========+
                | ID            | SERIAL       |   1       |  1        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | NAME          | VARCHAR(255) |   1       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | SCORE         | SCORES       |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | VOTES         | INTEGER      |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | INFO          | TEXT         |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | PHOTO         | VARCHAR(255) |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | ACTIVITY_ID   | INTEGER      |   0       |  0        |  1        |
                +---------------+--------------+-----------+-----------+-----------+
                | CITY_ID       | INTEGER      |   0       |  0        |  1        |
                +---------------+--------------+-----------+-----------+-----------+


.. code-block:: sql
    :linenos:

    CREATE TABLE Culture (
      ID SERIAL PRIMARY KEY,
      NAME VARCHAR(255) NOT NULL,
      SCORE SCORES DEFAULT 0,
      VOTES INTEGER DEFAULT 0,
      INFO TEXT,
      PHOTO VARCHAR(255),
      ACTIVITY_ID INTEGER REFERENCES Activities (ID) ON DELETE CASCADE,
      CITY_ID INTEGER REFERENCES Cities (ID) ON DELETE CASCADE
      )

1.1.3 Accommodation Table
+++++++++++++++++++++++++

                +---------------+---------------------+-----------+-----------+-----------+
                | Name          | Type                | Not Null  |Primary K. |Foreign K. |
                +===============+=====================+===========+===========+===========+
                | ID            | SERIAL              |   1       |  1        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | NAME          | VARCHAR(255)        |   1       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | SCORE         | SCORES              |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | VOTES         | INTEGER             |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | INFO          | TEXT                |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | PHOTO         | VARCHAR(255)        |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | TYPE          | ACCOMMODATION_TYPES |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | LOCATION_ID   | INTEGER             |   0       |  0        |  1        |
                +---------------+---------------------+-----------+-----------+-----------+


.. code-block:: sql
    :linenos:

      CREATE TABLE Accommodation (
         ID SERIAL PRIMARY KEY,
         NAME VARCHAR(255) NOT NULL,
         SCORE SCORES DEFAULT 0,
         VOTES INTEGER DEFAULT 0,
         INFO TEXT,
         PHOTO VARCHAR(255),
         TYPE ACCOMMODATION_TYPES,
         LOCATION_ID INTEGER REFERENCES Location (ID) ON DELETE CASCADE
         )

2 Code
======

2.1 Python(Flask) Files
-----------------------

2.1.1 Activities.py
+++++++++++++++++++

**Main Page**

.. code-block:: python
    :linenos:

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

**Details Page**

.. code-block:: python
    :linenos:

      @app.route('/activities/<int:id>')
      def activities_details(id):
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  statement = """SELECT * FROM Activities WHERE (ID = %s)"""
                  cursor.execute(statement, (id,))
                  activities_data = json.dumps(cursor.fetchall())
                  activities = json.loads(activities_data)
          return render_template('activities_details.html', activities=activities)

**Insert**

.. code-block:: python
    :linenos:

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

**Delete**

.. code-block:: python
    :linenos:

      @app.route('/activities/delete', methods=["POST"])
      def activities_delete():
          id = request.form["select"]
          id = int(id)
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  statement = """DELETE FROM Activities WHERE ID = (%s)"""
                  cursor.execute(statement, (id,))

          return redirect(url_for('activities_page'))

**Update**

.. code-block:: python
    :linenos:

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

**Delete All**

.. code-block:: python
    :linenos:

      @app.route('/activities/delete_all')
      def activities_delete_all():
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  query = """DELETE FROM Activities"""
                  cursor.execute(query)

          return redirect(url_for('activities_page'))


2.1.2 Culture.py
++++++++++++++++

**Main Page**

.. code-block:: python
    :linenos:

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

**Details Page**

.. code-block:: python
    :linenos:

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

**Insert**

.. code-block:: python
    :linenos:

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

**Delete**

.. code-block:: python
    :linenos:

      def culture_delete():
          id = request.form["select"]
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  statement = """DELETE FROM Culture WHERE ID = (%s)"""
                  cursor.execute(statement, (id))

          return redirect(url_for('culture_page'))

**Update**

.. code-block:: python
    :linenos:

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

**Delete All**

.. code-block:: python
    :linenos:

      @app.route('/culture/delete_all')
      def culture_delete_all():
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  query = """DELETE FROM Culture"""
                  cursor.execute(query)

          return redirect(url_for('culture_page'))

**Voting**

.. code-block:: python
    :linenos:

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

2.1.3 Accommodation.py
++++++++++++++++++++++

**Main Page**

.. code-block:: python
    :linenos:

      @app.route('/accommodation')
      def accommodation_page():
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  query = """SELECT Accommodation.ID, Accommodation.NAME, Accommodation.SCORE,
                             Accommodation.VOTES, Accommodation.INFO, Accommodation.PHOTO,
                             Accommodation.TYPE, Accommodation.LOCATION_ID, Countries.Name, Cities.Name,
                             Location.Name FROM Accommodation
                             LEFT OUTER JOIN Location
                             ON Accommodation.LOCATION_ID=Location.ID
                             LEFT OUTER JOIN Cities
                             ON Location.CITY=Cities.ID
                             LEFT OUTER JOIN Countries
                             ON Cities.COUNTRY=Countries.ID
                             ORDER BY SCORE DESC"""
                  cursor.execute(query)
                  places_data = json.dumps(cursor.fetchall())
                  places = json.loads(places_data)
                  for place in places:
                      place[2] = "{:2.2f}".format(place[2])

                  query = """SELECT ID,NAME FROM Location"""
                  cursor.execute(query)
                  locations_data = json.dumps(cursor.fetchall())
                  locations = json.loads(locations_data)

          if g.user:
              if(g.user == "admin"):
                  usernum = 0
              else:
                  usernum = 1
          else:
              usernum = 2
          now = datetime.datetime.now()
          return render_template('accommodation.html', current_time=now.ctime(), places=places, locations=locations, usernum=usernum)

**Details Page**

.. code-block:: python
    :linenos:

      @app.route('/accommodation/<int:id>')
      def accommodation_details(id):
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  statement = """SELECT Accommodation.ID, Accommodation.NAME, Accommodation.SCORE,
                                 Accommodation.VOTES, Accommodation.INFO, Accommodation.PHOTO,
                                 Accommodation.TYPE, Accommodation.LOCATION_ID, Countries.Name, Cities.Name,
                                 Location.Name FROM Accommodation
                                 LEFT OUTER JOIN Location
                                 ON Accommodation.LOCATION_ID=Location.ID
                                 LEFT OUTER JOIN Cities
                                 ON Location.CITY=Cities.ID
                                 LEFT OUTER JOIN Countries
                                 ON Cities.COUNTRY=Countries.ID
                                 WHERE (Accommodation.ID = %s)"""
                  cursor.execute(statement, (id,))
                  places_data = json.dumps(cursor.fetchall())
                  places = json.loads(places_data)

                  query = """SELECT ID,NAME FROM Location"""
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
          return render_template('accommodation_details.html', places=places, locations=locations, usernum=usernum)

**Insert**

.. code-block:: python
    :linenos:

      @app.route('/accommodation/insert', methods=["POST"])
      def accommodation_insert():
          name = request.form['accommodation_name']
          score = request.form['accommodation_place_score']
          votes = request.form['accommodation_place_votes']
          info = request.form['accommodation_info']
          photo = request.form['accommodation_photo']
          type = request.form['accommodation_type']
          location = request.form["accommodation_location"]
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  if name and score and votes and type and location:
                      query = """SELECT * FROM Location WHERE (ID = %s)"""
                      cursor.execute(query, (location,))
                      exists_data = json.dumps(cursor.fetchall())
                      exists = json.loads(exists_data)
                      if(exists):
                          statement = """INSERT INTO Accommodation (NAME, INFO, SCORE, VOTES, PHOTO, TYPE, LOCATION_ID)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                          cursor.execute(statement, (name,info,score,votes,photo,type,location))

          return redirect(url_for('accommodation_page'))

**Delete**

.. code-block:: python
    :linenos:

      @app.route('/accommodation/delete', methods=["POST"])
      def accommodation_delete():
          id = request.form["select"]
          id = int(id)
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  statement = """DELETE FROM Accommodation WHERE ID = (%s)"""
                  cursor.execute(statement, (id,))

          return redirect(url_for('accommodation_page'))

**Update**

.. code-block:: python
    :linenos:

      @app.route('/accommodation/update', methods=["POST"])
      def accommodation_update():
          name = request.form["accommodation_name_update"]
          photo = request.form["accommodation_photo_update"]
          info = request.form["accommodation_info_update"]
          type = request.form["accommodation_type_update"]
          location = request.form["accommodation_location_update"]
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
                  if location:
                      statement = """UPDATE Accommodation SET LOCATION_ID = (%s) WHERE (ID = %s)"""
                      cursor.execute(statement, (location,id))
          return redirect(url_for('accommodation_details',id=id))

**Delete All**

.. code-block:: python
    :linenos:

      @app.route('/accommodation/delete_all')
      def accommodation_delete_all():
          with dbapi2.connect(app.config['dsn']) as connection:
              with connection.cursor() as cursor:
                  query = """DELETE FROM Accommodation"""
                  cursor.execute(query)

          return redirect(url_for('accommodation_page'))

**Voting**

.. code-block:: python
    :linenos:

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
