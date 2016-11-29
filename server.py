from settings import *
from culture import *
from entertainment import *
from landmark import *
from caferest import *
from activities import *
from location import *

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP DOMAIN IF EXISTS SCORES CASCADE"""
        cursor.execute(query)

        query = """CREATE DOMAIN SCORES AS FLOAT
                    CHECK ((VALUE >= 0.0) AND (VALUE <= 10.0))"""
        cursor.execute(query)

        query = """DROP DOMAIN IF EXISTS ACTIVITY_TYPES CASCADE"""
        cursor.execute(query)

        query = """CREATE DOMAIN ACTIVITY_TYPES AS VARCHAR(255)
                    CHECK ((VALUE = 'Cultural') OR (VALUE = 'Eat & Drink')
                           OR (VALUE = 'Sport') OR (VALUE = 'Accommodation')
                           OR (VALUE = 'Travel'))"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Activities CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE Activities (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                INFO TEXT,
                PHOTO VARCHAR(255),
                TYPE ACTIVITY_TYPES
                )"""
        cursor.execute(query)

        query = """INSERT INTO Activities (NAME, INFO, PHOTO, TYPE)
                    VALUES ('Visit & Discover', 'To be added',
                            'https://thumb1.shutterstock.com/display_pic_with_logo/1070501/329988668/stock-photo-new-york-usa-sep-interior-of-the-metropolitan-museum-of-art-the-met-the-largest-art-329988668.jpg', 'Cultural'),
                           ('Attend & Watch', 'To be added',
                           'http://thumb101.shutterstock.com/display_pic_with_logo/476932/134693633/stock-photo-theater-interior-view-134693633.jpg', 'Cultural'),
                           ('Dine', 'To be added', 'https://thumb9.shutterstock.com/display_pic_with_logo/337030/282446912/stock-photo-table-set-restaurant-282446912.jpg', 'Eat & Drink'),
                           ('Breakfast & Brunch', 'To be added', 'http://theeverygirl.com/sites/default/files/articles/inlineimages/Everygirl%20Brunch_1034.jpg', 'Eat & Drink'),
                           ('Patisserie', 'To be added', 'http://c8.alamy.com/comp/BG82RM/france-paris-interior-of-a-patisserie-BG82RM.jpg', 'Eat & Drink'),
                           ('Drink (Alcohol)', 'To be added', 'https://thumb1.shutterstock.com/display_pic_with_logo/1433222/202914193/stock-photo-bar-and-desk-202914193.jpg', 'Eat & Drink'),
                           ('Swim', 'To be added', 'https://thumb9.shutterstock.com/display_pic_with_logo/764968/187844036/stock-photo-children-swimming-pool-187844036.jpg', 'Sport'),
                           ('Rest', 'To be added', 'https://thumb9.shutterstock.com/display_pic_with_logo/160510/123035896/stock-photo-hotel-room-123035896.jpg', 'Accommodation'),
                           ('Sightseeing', 'To be added', 'http://c8.alamy.com/comp/BHM71R/stanley-park-vancouver-bc-british-columbia-canada-sightseeing-tour-BHM71R.jpg', 'Travel'),
                           ('Transportaion', 'To be added', 'http://c8.alamy.com/comp/A9F95W/germany-berlin-a-hybrid-bus-belonging-to-the-city-s-transportation-A9F95W.jpg', 'Travel')"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Culture"""
        cursor.execute(query)

        query = """CREATE TABLE Culture (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                VOTES INTEGER DEFAULT 0,
                INFO TEXT,
                PHOTO VARCHAR(255),
                ACTIVITY_ID INTEGER REFERENCES Activities (ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO Culture (NAME, INFO, PHOTO, ACTIVITY_ID)
                    VALUES ('Great Wall of China', 'The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe. Several walls were being built as early as the 7th century BCE;[2] these, later joined together and made bigger and stronger, are now collectively referred to as the Great Wall.[3] Especially famous is the wall built 220â€“206 BCE by Qin Shi Huang, the first Emperor of China. Little of that wall remains. Since then, the Great Wall has on and off been rebuilt, maintained, and enhanced; the majority of the existing wall is from the Ming Dynasty (1368â€“1644).

Other purposes of the Great Wall have included border controls, allowing the imposition of duties on goods transported along the Silk Road, regulation or encouragement of trade and the control of immigration and emigration. Furthermore, the defensive characteristics of the Great Wall were enhanced by the construction of watch towers, troop barracks, garrison stations, signaling capabilities through the means of smoke or fire, and the fact that the path of the Great Wall also served as a transportation corridor.',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/240px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg',1),
                           ('SÃ¼reyya Opera House', 'SÃ¼reyya Opera House, also called SÃ¼reyya Cultural Center (Turkish: SÃ¼reyya OperasÄ± or SÃ¼reyya KÃ¼ltÃ¼r Merkezi), is an opera hall located in KadÄ±kÃ¶y district of Istanbul, Turkey. The building is designed by Armenian architect Kegam Kavafyan[1] by order of a Deputy for Istanbul SÃ¼reyya Ä°lmen, it was originally established in 1927 as the first musical theatre on the Anatolian part of Istanbul. However, due to lack of appropriate facilities and equipment in the theatre, operettas were never staged. The venue was rather used as a movie theatre until the building underwent a functional restoration and reopened as an opera house by the end of 2007.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/20131207_Istanbul_076.jpg/250px-20131207_Istanbul_076.jpg', 2),
                           ('Hagia Sophia', 'Hagia Sophia (from the Greek: á¼‰Î³Î¯Î± Î£Î¿Ï†Î¯Î±, [aËˆÊ�ia soËˆfia]), "Holy Wisdom"; Latin: Sancta Sophia or Sancta Sapientia; Turkish: Ayasofya) was a Greek Orthodox Christian patriarchal basilica (church), later an imperial mosque, and now a museum (Ayasofya MÃ¼zesi) in Istanbul, Turkey. From the date of its construction in 537 AD, and until 1453, it served as an Eastern Orthodox cathedral and seat of the Patriarch of Constantinople,[1] except between 1204 and 1261, when it was converted by the Fourth Crusaders to a Catholic cathedral under the Latin Empire. The building was later converted into an Ottoman mosque from 29 May 1453 until 1931. It was then secularized and opened as a museum on 1 February 1935.[2]

Famous in particular for its massive dome, it is considered the epitome of Byzantine architecture[3] and is said to have "changed the history of architecture".[4] It remained the world''s largest cathedral for nearly a thousand years, until Seville Cathedral was completed in 1520.

The current building was originally constructed as a church between 532 and 537 on the orders of the Byzantine Emperor Justinian I and was the third Church of the Holy Wisdom to occupy the site, the previous two having both been destroyed by rioters. It was designed by the Greek geometers Isidore of Miletus and Anthemius of Tralles.[5]

The church was dedicated to the Wisdom of God, the Logos, the second person of the Trinity,[6] its patronal feast taking place on 25 December, the commemoration of the birth of the incarnation of the Logos in Christ.[6] Although sometimes referred to as Sancta Sophia (as though it were named after Sophia the Martyr), sophia being the phonetic spelling in Latin of the Greek word for wisdom, its full name in Greek is Î�Î±á½¸Ï‚ Ï„á¿†Ï‚ á¼‰Î³Î¯Î±Ï‚ Ï„Î¿á¿¦ Î˜ÎµÎ¿á¿¦ Î£Î¿Ï†Î¯Î±Ï‚, Naos tÄ“s Hagias tou Theou Sophias, "Shrine of the Holy Wisdom of God".[7][8] The church contained a large collection of relics and featured, among other things, a 15-metre (49 ft) silver iconostasis. The focal point of the Eastern Orthodox Church for nearly one thousand years, the building witnessed the excommunication of Patriarch Michael I Cerularius on the part of Humbert of Silva Candida, the papal envoy of Pope Leo IX in 1054, an act that is commonly considered the start of the Eastâ€“West Schism.',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Hagia_Sophia_Mars_2013.jpg/220px-Hagia_Sophia_Mars_2013.jpg',1),
                           ('Broadway Theatre (53rd Street)', 'The Broadway Theatre (formerly Universal''s Colony Theatre, B.S. Moss'' Broadway Theatre, Earl Carroll''s Broadway Theatre, and CinÃ© Roma) is a Broadway theatre located in midtown Manhattan. It has a large seating capacity of 1,761, and unlike most Broadway theaters, it is actually located on Broadway, at number 1681.

Designed by architect Eugene De Rosa for Benjamin S. Moss, it opened as B.S. Moss''s Colony Theatre on Christmas Day 1924 as a venue for vaudeville shows and motion pictures. The theater has operated under many names and owners. It was renamed Universal''s Colony Theatre, B.S. Moss'' Broadway Theatre, and Earl Carroll''s Broadway Theatre before becoming a legitimate theater house simply called Broadway Theatre on December 8, 1930. In 1937, known as CinÃ© Roma, it showed Italian films.[1] For a short time during the 1950s it showed Cinerama films.[2]

On November 18, 1928 the first Mickey Mouse cartoon released to the public, Steamboat Willie, debuted at the Colony. Producer Walt Disney returned on November 13, 1940 to debut the feature film Fantasia in Fantasound, an early stereo system.
The legitimate theater opened in 1930 with The New Yorkers by Cole Porter. Stars such as Milton Berle, Alfred Drake, JosÃ© Ferrer, Eartha Kitt, Vivien Leigh, Zero Mostel, and Mae West have appeared on stage.[1]

The Shubert Organization bought the theater in 1939 and renovated it extensively in 1956 and 1986. It has long been a popular theatre for producers of musicals because of large seating capacity, and the large stage, which is nearly sixty feet deep. Often plays that have become successful in smaller theaters have transferred to the Broadway Theatre.[1]',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Promises_Promises_at_Broadway_Theatre.JPG/220px-Promises_Promises_at_Broadway_Theatre.JPG',2)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Entertainment"""
        cursor.execute(query)

        query = """CREATE TABLE Entertainment(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                PLACE VARCHAR(255) NULL,
                SCORE FLOAT NULL
                )"""
        cursor.execute(query)

        query = """INSERT INTO Entertainment(NAME, PLACE,SCORE)
                    VALUES ('Semerkant', 'Taksim', 6.5),
                           ('Cati', 'Resitpasa', 6.0),
                           ('Beat', 'Taksim', 8.0)"""
        cursor.execute(query)

            ##################################################################

        query = """DROP TABLE IF EXISTS PEOPLE CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE PEOPLE (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SURNAME VARCHAR(255) NOT NULL
                )"""
        cursor.execute(query)

        query = """INSERT INTO PEOPLE (NAME, SURNAME)
                    VALUES ('Fatih ', 'Budak '),
                           ('Güray ', 'Ocak '),
                           ('Mehmet ', 'Özen '),
                           ('Berkan ', 'Dinar ')"""
        cursor.execute(query)
            ###########

        query = """DROP TABLE IF EXISTS LOCATION CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE LOCATION (
                ID SERIAL PRIMARY KEY,
                CITYNAME VARCHAR(255) UNIQUE NOT NULL
                )"""
        cursor.execute(query)

        query = """INSERT INTO LOCATION (CITYNAME)
                    VALUES ('Istanbul '),
                           ( 'New York '),
                           ('Pisa '),
                           ( 'Rio de Janeiro '),
                           ( 'London '),
                           ( 'Barcelona '),
                           ( 'Paris '),
                           ('Moscow '),
                           ( 'Koln ')"""
        cursor.execute(query)
            ###########

        query = """DROP TABLE IF EXISTS LANDMARK"""
        cursor.execute(query)

        query = """CREATE TABLE LANDMARK (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                LOCATIONID INTEGER REFERENCES LOCATION(ID) ON DELETE CASCADE,
                BYWHOMID INTEGER REFERENCES PEOPLE(ID) ON DELETE CASCADE,
                INFO TEXT
                )"""
        cursor.execute(query)

        query = """INSERT INTO LANDMARK (NAME, SCORE, LOCATIONID, BYWHOMID, INFO)
                    VALUES ('Maiden Tower ', 9.9, 1, 1, 'Information of Maiden Tower '),
                           ('Statue of Liberty ', 8.7, 2, 2, 'Information of Statue of Liberty '),
                           ('Leaning Tower of Pisa ', 7.2, 3, 3, 'Information of Leaning Tower of Pisa'),
                           ('Christ the Redeemer ', 5.7, 4, 4, 'Information of Christ the Redeemer')"""
        cursor.execute(query)
            ###########

        query = """DROP TABLE IF EXISTS USERS"""
        cursor.execute(query)

        query = """CREATE TABLE USERS (
                ID SERIAL PRIMARY KEY REFERENCES PEOPLE(ID) ON DELETE CASCADE,
                USERNAME VARCHAR(255) NOT NULL,
                EMAIL VARCHAR(255) NOT NULL,
                AGE INTEGER,
                WHENCE INTEGER REFERENCES LOCATION(ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO USERS (USERNAME, EMAIL, AGE, WHENCE)
                    VALUES ('budakf ', 'email of budakf ', 24, 1),
                           ('ocakg ', 'email of ocakg ', 24, 2),
                           ('ttozen ', 'email of ttozen ', 23, 3),
                           ('dinar ', 'email of dinar ', 22, 4)"""
        cursor.execute(query)
            ###########

            ##################################################################

        query = """DROP TABLE IF EXISTS CafeRest"""
        cursor.execute(query)

        query = """CREATE TABLE CafeRest (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                CITY VARCHAR(255) NOT NULL,
                CUISINE VARCHAR(255) NULL,
                SCORE FLOAT
                )"""
        cursor.execute(query)

        query = """INSERT INTO CafeRest (NAME, CITY, CUISINE, SCORE)
                    VALUES ('Le Cinq', 'Paris', 'French', 9.2),
                           ('The Ledbury', 'London', 'European', 8.7),
                           ('Lekker Cafe Restaurant', 'Istanbul', 'Turkish', 9.4)"""
        cursor.execute(query)


        connection.commit()
    return redirect(url_for('home_page'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count

@app.route('/agency')
def agency_page():
    now = datetime.datetime.now()
    return render_template('agency.html', current_time=now.ctime())

if __name__ == '__main__':

    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
