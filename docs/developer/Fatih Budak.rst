Parts Implemented by Fatih Budak
********************************

1 Database Design
=================

**3 tables(People, Landmark and Agency) are implemented by Fatih Budak**

**People and Landmark tables have foreign key**

1.1 Database Tables
-------------------

1.1.1 People Table
++++++++++++++++++

* **People** table has four foreign keys. "Whence_id" is related to location table "Best_activity_id" is related to activity table, "Best_place_id" is related to location table and "Best_culture_id" is related to culture table.


                +------------------+----------------+-----------+-----------+-----------+
                | Name             | Type           | Not Null  |Primary K. |Foreign K. |
                +==================+================+===========+===========+===========+
                | ID               | SERIAL         |   1       |  1        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | NAME             | VARCHAR(255)   |   1       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | SURNAME          | VARCHAR(255)   |   1       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | USERNAME         | VARCHAR(255)   |   1       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | PASSWORD         | VARCHAR(255)   |   1       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | EMAIL            | VARCHAR(255)   |   0       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | AGE              | INTEGER        |   0       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | WHENCE_ID        | INTEGER        |   0       |  0        |  1        |
                +------------------+----------------+-----------+-----------+-----------+
                | PHOTO            | VARCHAR(255)   |   0       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+
                | BEST_ACTIVITY_ID | INTEGER        |   0       |  0        |  1        |
                +------------------+----------------+-----------+-----------+-----------+
                | BEST_PLACE_ID    | INTEGER        |   0       |  0        |  1        |
                +------------------+----------------+-----------+-----------+-----------+
                | BEST_CULTURE_ID  | INTEGER        |   0       |  0        |  1        |
                +------------------+----------------+-----------+-----------+-----------+
                | ISACTIVE         | BOOLEAN        |   0       |  0        |  0        |
                +------------------+----------------+-----------+-----------+-----------+

* Postgresql Implementation of **People Table**:

.. code-block:: sql
    :linenos:

      CREATE TABLE PEOPLE (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SURNAME VARCHAR(255) NOT NULL,
                USERNAME VARCHAR(255) UNIQUE NOT NULL,
                PASSWORD VARCHAR(255) NOT NULL,
                EMAIL VARCHAR(255),
                AGE INTEGER,
                WHENCE_ID INTEGER REFERENCES Cities(ID) ON DELETE CASCADE,
                PHOTO VARCHAR(255),
                BEST_ACTIVITY_ID INTEGER REFERENCES Activities(ID) ON DELETE CASCADE,
                BEST_PLACE_ID INTEGER REFERENCES Location(ID) ON DELETE CASCADE,
                BEST_CULTURE_ID INTEGER REFERENCES Culture(ID) ON DELETE CASCADE,
                ISACTIVE BOOLEAN DEFAULT FALSE
                }

1.1.2 Landmark Table
++++++++++++++++++++

* **Landmark** table has one foreign key relationship with location table

                +---------------+--------------+-----------+-----------+-----------+
                | Name          | Type         | Not Null  |Primary K. |Foreign K. |
                +===============+==============+===========+===========+===========+
                | ID            | SERIAL       |   1       |  1        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | NAME          | VARCHAR(255) |   1       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | SCORE         | SCORES       |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | PHOTO         | VARCHAR(255) |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | LOCATION_ID   | INTEGER      |   0       |  0        |  1        |
                +---------------+--------------+-----------+-----------+-----------+
                | VOTES         | INTEGER      |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+
                | INFO          | TEXT         |   0       |  0        |  0        |
                +---------------+--------------+-----------+-----------+-----------+

* Postgresql Implementation of **Landmark Table**:

.. code-block:: sql
    :linenos:

      CREATE TABLE LANDMARK (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                PHOTO VARCHAR(255),
                LOCATIONID INTEGER REFERENCES Cities(ID) ON DELETE CASCADE,
                VOTES INTEGER DEFAULT 0,
                INFO TEXT
                )

1.1.3 Agency Table
++++++++++++++++++

* **Agency** table does not use a foreign key

                +---------------+---------------------+-----------+-----------+-----------+
                | Name          | Type                | Not Null  |Primary K. |Foreign K. |
                +===============+=====================+===========+===========+===========+
                | ID            | SERIAL              |   1       |  1        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | NAME          | VARCHAR(255)        |   1       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | SCORE         | SCORES              |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | PHOTO         | VARCHAR(255)        |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | VOTES         | INTEGER             |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+
                | INFO          | TEXT                |   0       |  0        |  0        |
                +---------------+---------------------+-----------+-----------+-----------+

* Postgresql Implementation of **Agency Table**:

.. code-block:: sql
    :linenos:

      CREATE TABLE AGENCY(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                PHOTO VARCHAR(255),
                VOTES INTEGER DEFAULT 0,
                INFO TEXT
                )


2 Code
======

2.1 Python(Flask) Files
-----------------------

2.1.1 Register.py
+++++++++++++++++

* This file used to register new user and to complete profile information of new user.

**Register Page**

.. code-block:: python
    :linenos:

      @app.route('/registration/register', methods=["POST"])
      def register_operation():
          name = request.form['name']
          surname = request.form['surname']
          username = request.form['user_name']
          password = request.form['pass']
          repassword = request.form['repass']
          #default photo
          photo ='http://previews.123rf.com/images/richcat/richcat1109/richcat110900082/10732608-Graphic-illustration-of-man-in-business-suit-as-user-icon-avatar-Stock-Vector.jpg'
          with dbapi2.connect(app.config['dsn']) as connection:
               with connection.cursor() as cursor:
                  if username:
                        query = """SELECT PEOPLE.USERNAME FROM PEOPLE
                        WHERE (PEOPLE.USERNAME = %s)"""
                  cursor.execute(query,(username, ))
                  user_data = json.dumps(cursor.fetchall())
                  exist = json.loads(user_data)

                  if exist:
                        return redirect(url_for('register_page'))

                  if name and surname and username and (password == repassword):
                        statement = """INSERT INTO PEOPLE (NAME, SURNAME, USERNAME, PASSWORD, PHOTO)
                        VALUES (%s,%s,%s,%s,%s )"""
                  cursor.execute(statement, (name,surname,username,password,photo ))

                  elif (password != repassword):
                  ##flash ('Password Conflict') ##
                        return redirect(url_for('register_page'))

         return redirect(url_for('new_user_page',username=username))

**New User Page**

.. code-block:: python
    :linenos:

      @app.route('/welcome/<username>')
      def new_user_page(username):
         with dbapi2.connect(app.config['dsn']) as connection:
               with connection.cursor() as cursor:
                  query = """SELECT PEOPLE.ID, PEOPLE.NAME, PEOPLE.SURNAME,
                           PEOPLE.USERNAME, PEOPLE.PHOTO FROM PEOPLE
                           WHERE (PEOPLE.USERNAME = %s)"""
                  cursor.execute(query,(username, ))
                  user_data = json.dumps(cursor.fetchall())
                  user = json.loads(user_data)
                    ##########################################################

                  query = """SELECT ID, NAME FROM Cities"""
                  cursor.execute(query)
                  city_data = json.dumps(cursor.fetchall())
                  city = json.loads(city_data)

                    ##########################################################
                  query = """SELECT ID, NAME FROM Culture"""
                  cursor.execute(query)
                  culture_data = json.dumps(cursor.fetchall())
                  culture = json.loads(culture_data)

                    ##########################################################
                  query = """SELECT ID, NAME FROM Activities"""
                  cursor.execute(query)
                  activity_data = json.dumps(cursor.fetchall())
                  activity = json.loads(activity_data)

                    ##########################################################

                  query = """SELECT ID, NAME FROM Location"""
                  cursor.execute(query)
                  location_data = json.dumps(cursor.fetchall())
                  location = json.loads(location_data)

            return render_template('new_user.html',user=user, city=city, culture=culture, activity=activity, location=location)


**Complete Profile Page**

.. code-block:: python
    :linenos:

      @app.route('/welcome' , methods=["POST"])
      def add_info():
         email = request.form['email']
         age = request.form['age']
         age=int(age);
         photo = request.form['photo']
         whence = request.form['whence']
         activity_type = request.form['activity_type']
         activity = request.form['activity']
         district = request.form['district']
         id = request.form['user_index']

         with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                  if email:
                     statement = """UPDATE PEOPLE SET (EMAIL) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (email,id ))

                  if age:
                     statement = """UPDATE PEOPLE SET (AGE) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (age,id  ))

                  if photo:
                     statement = """UPDATE PEOPLE SET (PHOTO) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (photo,id  ))

                  if whence:
                     statement = """UPDATE PEOPLE SET (WHENCE_ID) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (whence,id  ))

                  if activity_type:
                     statement = """UPDATE PEOPLE SET (BEST_CULTURE_ID) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (activity_type,id  ))

                  if activity:
                     statement = """UPDATE PEOPLE SET (BEST_ACTIVITY_ID) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (activity,id  ))

                  if district:
                     statement = """UPDATE PEOPLE SET (BEST_PLACE_ID) = (%s) WHERE (ID = %s)"""
                     cursor.execute(statement, (district,id  ))

            return redirect(url_for('people_page',id=id))


2.1.2 People.py
+++++++++++++++

* This file is used to display user profile page.

**User Page**

.. code-block:: python
    :linenos:

      @app.route('/people/<int:id>')
      def people_page(id):
          with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
            query = """SELECT PEOPLE.ID, PEOPLE.NAME, PEOPLE.SURNAME,
                        PEOPLE.USERNAME, PEOPLE.EMAIL, PEOPLE.AGE, PEOPLE.PHOTO,
                        PEOPLE.WHENCE_ID, Cities.NAME FROM PEOPLE
                        LEFT OUTER JOIN Cities
                        ON PEOPLE.WHENCE_ID=Cities.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            people_data = json.dumps(cursor.fetchall())
            people = json.loads(people_data)
                    ##########################################################

            query = """SELECT Activities.NAME, Activities.INFO FROM PEOPLE
                        LEFT OUTER JOIN Activities
                        ON PEOPLE.BEST_ACTIVITY_ID=Activities.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            activity_data = json.dumps(cursor.fetchall())
            activity = json.loads(activity_data)

            query = """SELECT ID, NAME FROM Cities"""
            cursor.execute(query)
            location_data = json.dumps(cursor.fetchall())
            location = json.loads(location_data)
                     ##########################################################

            query = """SELECT Location.NAME, Location.INFO, Location.Photo FROM PEOPLE
                        LEFT OUTER JOIN Location
                        ON PEOPLE.BEST_PLACE_ID=Location.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            place_data = json.dumps(cursor.fetchall())
            place = json.loads(place_data)
                    ##########################################################

            query = """SELECT Culture.NAME, Culture.INFO, Culture.Photo FROM PEOPLE
                        LEFT OUTER JOIN Culture
                        ON PEOPLE.BEST_CULTURE_ID=Culture.ID WHERE (PEOPLE.ID = %s)"""
            cursor.execute(query, (id, ))
            culture_data = json.dumps(cursor.fetchall())
            culture = json.loads(culture_data)
                    ##########################################################


       now = datetime.datetime.now()
       return render_template('people.html', people=people, location=location, activity=activity, place=place, culture=culture)





2.1.3 Landmark.py
+++++++++++++++++

* This file is used to display landmarks list. Also, thanks to this file, on landmark table, insert, delete, update and delete all operations are done by only admin. Addition to this, this file also have voting function.

**Main Page**

.. code-block:: python
    :linenos:

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



**Details Page**

.. code-block:: python
    :linenos:

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


**Insert**

.. code-block:: python
    :linenos:

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



**Delete**

.. code-block:: python
    :linenos:

      @app.route('/landmark/delete', methods=["POST"])
      def landmark_delete():
         id = request.form["select"]
         with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                  statement = """DELETE FROM LANDMARK WHERE ID = (%s)"""
                  cursor.execute(statement, (id))

         return redirect(url_for('landmark_page'))



**Update**

.. code-block:: python
    :linenos:

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


**Delete All**

.. code-block:: python
    :linenos:

      @app.route('/landmark/delete_all')
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


**Voting**

.. code-block:: python
    :linenos:

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


2.1.4 Agency.py
+++++++++++++++

* This file is used to display agencies list. Also, thanks to this file, on agency table, insert, delete, update and delete all operations are done by only admin. Addition to this, this file also have voting function.


**Main Page**

.. code-block:: python
    :linenos:

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


**Details Page**

.. code-block:: python
    :linenos:

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


**Insert**

.. code-block:: python
    :linenos:

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



**Delete**

.. code-block:: python
    :linenos:

      @app.route('/agency/delete', methods=["POST"])
      def agency_delete():
         id = request.form["select"]
         with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
               statement = """DELETE FROM AGENCY WHERE ID = (%s)"""
               cursor.execute(statement, (id))

         return redirect(url_for('agency_page'))


**Update**

.. code-block:: python
    :linenos:

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



**Delete All**

.. code-block:: python
    :linenos:

      @app.route('/agency/delete_all')
      def agency_delete_all():
         with dbapi2.connect(app.config['dsn']) as connection:
            with connection.cursor() as cursor:
                  query = """DELETE FROM AGENCY"""
                  cursor.execute(query)

         return redirect(url_for('agency_page'))



**Voting**

.. code-block:: python
    :linenos:

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

2.1.5 Server.py
+++++++++++++++

**Login**

* Login function provides admin and users to enter the web site succesfully.

.. code-block:: python
    :linenos:

      @app.route('/login', methods=['GET','POST'])
      def login_page():
         T=True
         id=1
         if request.method == 'POST':
            if(g.user):
                  session.pop('user', None)
                  with dbapi2.connect(app.config['dsn']) as connection:
                     with connection.cursor() as cursor:
                        statement = """SELECT PEOPLE.ID, PEOPLE.USERNAME FROM PEOPLE WHERE(PEOPLE.USERNAME = %s)"""
                        cursor.execute(statement, (g.user,))
                        current_user_data = json.dumps(cursor.fetchall())
                        current_user = json.loads(current_user_data)
                        statement = """UPDATE PEOPLE SET (ISACTIVE) = (%s) WHERE(ID = %s)"""
                        T=False
                        cursor.execute(statement, (T,current_user[0][0] ) )

                  with dbapi2.connect(app.config['dsn']) as connection:
                     with connection.cursor() as cursor:
                        statement = """SELECT PEOPLE.ID, PEOPLE.USERNAME, PEOPLE.PASSWORD, PEOPLE.ISACTIVE FROM PEOPLE"""
                        cursor.execute(statement)

                        user_data = json.dumps(cursor.fetchall())
                        users = json.loads(user_data)

                  for user in users:
                     if  request.form['username'] == user[1]:
                         if  request.form['password'] == user[2]:
                             if user[3]==False:
                                id=user[0]
                                statement = """UPDATE PEOPLE SET (ISACTIVE) = (%s) WHERE(ID = %s) """
                                T=True
                                cursor.execute(statement, (T,id ) )
                                session['user'] = user[1]
                                return redirect(url_for('home_page'))

                  return render_template('login.html')

**Logout**

* Login function provides admin and users to exit the web site safely.

.. code-block:: python
    :linenos:

      @app.route('/logout')
      def logout_page():
         T=False
         if(g.user):
            session.pop('user', None)
            with dbapi2.connect(app.config['dsn']) as connection:
               with connection.cursor() as cursor:
                  statement = """SELECT PEOPLE.ID, PEOPLE.USERNAME FROM PEOPLE WHERE(PEOPLE.USERNAME = %s)"""
                  cursor.execute(statement, (g.user,))
                  current_user_data = json.dumps(cursor.fetchall())
                  current_user = json.loads(current_user_data)
                  if(current_user):
                     statement = """UPDATE PEOPLE SET (ISACTIVE) = (%s) WHERE(ID = %s)"""
                     cursor.execute(statement, (T,current_user[0][0] ) )
            return redirect(url_for('home_page'))

