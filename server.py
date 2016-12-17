from settings import *
from culture import *
from entertainment import *
from transportation import *
from activities import *
from location import *
from landmark import *
from people import *
from users import *
from register import *
from agency import *

@app.route('/')
def home_page():
    if g.user:
        if (g.user == "admin"):
            usernum = 0
        else:
            usernum = 1
    else:
        usernum = 2
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime(), usernum=usernum)

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

        query = """DROP DOMAIN IF EXISTS FESTIVALS CASCADE"""
        cursor.execute(query)

        query = """CREATE DOMAIN FESTIVALS AS VARCHAR(255)
                    CHECK ((VALUE = 'Music') OR (VALUE = 'Food')
                           OR (VALUE = 'Film') OR (VALUE = 'Art')
                           OR (VALUE = 'Seasonal'))"""
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

        query = """DROP TABLE IF EXISTS Culture CASCADE"""
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
                    VALUES ('Great Wall of China', 'The Great Wall of China is a series of fortifications made of stone, brick, tamped earth, wood, and other materials, generally built along an east-to-west line across the historical northern borders of China to protect the Chinese states and empires against the raids and invasions of the various nomadic groups of the Eurasian Steppe. Several walls were being built as early as the 7th century BCE;[2] these, later joined together and made bigger and stronger, are now collectively referred to as the Great Wall.[3] Especially famous is the wall built 220ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“206 BCE by Qin Shi Huang, the first Emperor of China. Little of that wall remains. Since then, the Great Wall has on and off been rebuilt, maintained, and enhanced; the majority of the existing wall is from the Ming Dynasty.

Other purposes of the Great Wall have included border controls, allowing the imposition of duties on goods transported along the Silk Road, regulation or encouragement of trade and the control of immigration and emigration. Furthermore, the defensive characteristics of the Great Wall were enhanced by the construction of watch towers, troop barracks, garrison stations, signaling capabilities through the means of smoke or fire, and the fact that the path of the Great Wall also served as a transportation corridor.',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/The_Great_Wall_of_China_at_Jinshanling-edit.jpg/240px-The_Great_Wall_of_China_at_Jinshanling-edit.jpg',1),
                           ('Süreyya Opera House', 'Sureyya Opera House, also called Sureyya Cultural Center (Turkish: Sureyya Operasi or Sureyya Kultur Merkezi), is an opera hall located in Kadikoy district of Istanbul, Turkey. The building is designed by Armenian architect Kegam Kavafyan[1] by order of a Deputy for Istanbul Sureyya Ilmen, it was originally established in 1927 as the first musical theatre on the Anatolian part of Istanbul. However, due to lack of appropriate facilities and equipment in the theatre, operettas were never staged. The venue was rather used as a movie theatre until the building underwent a functional restoration and reopened as an opera house by the end of 2007.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/20131207_Istanbul_076.jpg/250px-20131207_Istanbul_076.jpg', 2),
                           ('Hagia Sophia', '"Holy Wisdom"; Latin: Sancta Sophia or Sancta Sapientia; Turkish: Ayasofya) was a Greek Orthodox Christian patriarchal basilica (church), later an imperial mosque, and now a museum (Ayasofya Muzesi) in Istanbul, Turkey. From the date of its construction in 537 AD, and until 1453, it served as an Eastern Orthodox cathedral and seat of the Patriarch of Constantinople,[1] except between 1204 and 1261, when it was converted by the Fourth Crusaders to a Catholic cathedral under the Latin Empire. The building was later converted into an Ottoman mosque from 29 May 1453 until 1931. It was then secularized and opened as a museum on 1 February 1935.[2]

Famous in particular for its massive dome, it is considered the epitome of Byzantine architecture[3] and is said to have "changed the history of architecture".[4] It remained the world''s largest cathedral for nearly a thousand years, until Seville Cathedral was completed in 1520.

The current building was originally constructed as a church between 532 and 537 on the orders of the Byzantine Emperor Justinian I and was the third Church of the Holy Wisdom to occupy the site, the previous two having both been destroyed by rioters. It was designed by the Greek geometers Isidore of Miletus and Anthemius of Tralles.',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Hagia_Sophia_Mars_2013.jpg/220px-Hagia_Sophia_Mars_2013.jpg',1),
                           ('Broadway Theatre (53rd Street)', 'The Broadway Theatre (formerly Universal''s Colony Theatre, B.S. Moss'' Broadway Theatre, Earl Carroll''s Broadway Theatre) is a Broadway theatre located in midtown Manhattan. It has a large seating capacity of 1,761, and unlike most Broadway theaters, it is actually located on Broadway, at number 1681.

Designed by architect Eugene De Rosa for Benjamin S. Moss, it opened as B.S. Moss''s Colony Theatre on Christmas Day 1924 as a venue for vaudeville shows and motion pictures. The theater has operated under many names and owners. It was renamed Universal''s Colony Theatre, B.S. Moss'' Broadway Theatre, and Earl Carroll''s Broadway Theatre before becoming a legitimate theater house simply called Broadway Theatre on December 8, 1930. In 1937, it showed Italian films.[1] For a short time during the 1950s it showed Cinerama films.[2]

On November 18, 1928 the first Mickey Mouse cartoon released to the public, Steamboat Willie, debuted at the Colony. Producer Walt Disney returned on November 13, 1940 to debut the feature film Fantasia in Fantasound, an early stereo system.
The legitimate theater opened in 1930 with The New Yorkers by Cole Porter. Stars such as Milton Berle, Alfred Drake, Jose Ferrer, Eartha Kitt, Vivien Leigh, Zero Mostel, and Mae West have appeared on stage.[1]

The Shubert Organization bought the theater in 1939 and renovated it extensively in 1956 and 1986. It has long been a popular theatre for producers of musicals because of large seating capacity, and the large stage, which is nearly sixty feet deep. Often plays that have become successful in smaller theaters have transferred to the Broadway Theatre.[1]',
                            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Promises_Promises_at_Broadway_Theatre.JPG/220px-Promises_Promises_at_Broadway_Theatre.JPG',2)"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Countries CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE Countries (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                INFO TEXT,
                PHOTO VARCHAR(255)
                )"""
        cursor.execute(query)

        query = """INSERT INTO Countries (NAME, INFO, PHOTO)
                    VALUES  ('Turkey', 'To be added', 'http://center-maxima.com/wp-content/uploads/2014/02/turkey.jpg'),
                            ('Germany', 'To be added', 'https://s-media-cache-ak0.pinimg.com/originals/81/a2/61/81a2617c60520a95701cf34834966035.png'),
                            ('USA', 'To be added', 'http://www.cambridgedu.com/images/img/usa.png'),
                            ('Italy', 'To be added', 'https://s-media-cache-ak0.pinimg.com/originals/81/a2/61/81a2617c60520a95701cf34834966035.png'),
                            ('Brasil', 'To be added', 'http://www.cambridgedu.com/images/img/usa.png')"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Cities CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE Cities (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                INFO TEXT,
                PHOTO VARCHAR(255),
                COUNTRY INTEGER REFERENCES Countries (ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO Cities (NAME, INFO, PHOTO, COUNTRY)
                    VALUES  ('İstanbul', 'To be added', 'https://lh6.googleusercontent.com/--whYuqd2Zso/U5gZkZxQMmI/AAAAAAAAu-E/A4VH6Cr2IX8/s1152/k%25C4%25B1zkulaesi.jpg', 1),
                            ('Edirne', 'To be added', 'https://www.era111.com/files/import/images/en-guzel-edirne-resimleri.jpeg', 1),
                            ('Berlin', 'To be added', 'http://www.easyjet.com/en/holidays/shared/images/guides/germany/berlin.jpg', 2),
                            ('San Francisco', 'To be added', 'http://www.mrwallpaper.com/wallpapers/san-francisco-1600x900.jpg', 3),
                            ('Ankara', 'To be Added', 'http://www.neredekal.com/res/haber/hb_b_20115444_l-b.jpg', 1),
                            ('İstanbul', 'To be added ', 'https://lh6.googleusercontent.com/--whYuqd2Zso/U5gZkZxQMmI/AAAAAAAAu-E/A4VH6Cr2IX8/s1152/k%25C4%25B1zkulaesi.jpg', 1),
                            ('New York', ' To be added', 'https://www.era111.com/files/import/images/en-guzel-edirne-resimleri.jpeg', 3),
                            ('Pisa', 'To be added ', 'http://www.easyjet.com/en/holidays/shared/images/guides/germany/berlin.jpg', 3),
                            ('Rio de Janeiro', 'To be added ', 'http://www.mrwallpaper.com/wallpapers/san-francisco-1600x900.jpg', 4)
                            """
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Location CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE Location (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                INFO TEXT,
                PHOTO VARCHAR(255) DEFAULT 'https://d30y9cdsu7xlg0.cloudfront.net/png/1832-200.png',
                CITY INTEGER REFERENCES Cities (ID) ON DELETE CASCADE,
                COUNTRY INTEGER REFERENCES Countries (ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO Location (NAME, PHOTO, CITY, COUNTRY)
                    VALUES  ('Kadıköy', 'http://www.tatil.com/cmsImage/1449131787kadikoy2__730x352.jpg', 1, 2),
                            ('Tophane', 'http://www.hurriyetdailynews.com/images/news/201311/n_57635_1.jpg', 1, 2),
                            ('Taksim', 'http://www.tatiluzmani.tv/wp-content/uploads/2015/03/Taksim.jpg', 1, 2),
                            ('Şişli', 'http://www.sislibocekilaclama.gen.tr/wp-content/uploads/2015/01/sisli.png', 1, 2),
                            ('Reşitpaşa', 'http://www.sariyerposta.com/wp-content/uploads/32618398.jpg', 1, 2),
                            ('Uzunköprü', 'http://www.gezilecekyerler.biz/wp-content/uploads/2016/08/Uzunk%C3%B6pr%C3%BC-Hangi-%C5%9Eehirde.jpg', 2, 2),
                            ('San Jose', 'http://www.sanjoseca.gov/images/pages/N1736/DowntownSummer2005%20edited%20(1).JPG', 4, 3),
                            ('Reinickendorf', 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Ratusz_Reinickendorf.jpg', 3, 2),
                            ('Esenler', 'http://i.milliyet.com.tr/YeniAnaResim/2015/05/26/fft99_mf5675408.Jpeg', 1, 2),
                            ('Bakırköy', 'http://elmasilaclama.com/bocek-ilaclama/bakirkoy-fare-ilaclama.jpg', 1, 2),
                            ('Pendik', 'http://i.sozcu.com.tr/wp-content/uploads/2016/01/04/pendik-dha.jpg', 1, 2),
                            ('Akyurt-Çubuk', 'https://www.projepedia.com/media/upload/ANKARA/akyurt-ulasim.jpg', 5, 2)
                            """
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Entertainment"""
        cursor.execute(query)

        query = """CREATE TABLE Entertainment(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                VOTES INTEGER DEFAULT 0,
                INFO TEXT,
                PHOTO VARCHAR(255) DEFAULT 'https://cdn3.iconfinder.com/data/icons/glypho-movie-and-video/64/theater-masks-512.png',
                ACTIVITY INTEGER REFERENCES Activities (ID) ON DELETE CASCADE,
                PLACE INTEGER REFERENCES Location (ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO Entertainment(NAME,INFO,PHOTO,ACTIVITY,PLACE)
                    VALUES ('İstanbul Modern', 'İstanbul Modern, aka Istanbul Museum of Modern Art, (Turkish: İstanbul Modern Sanat Müzesi) is a museum of contemporary art in the BeyoÄŸlu district of Istanbul, Turkey. Inaugurated on December 11, 2004, the museum features the work of Turkish artists. The director of the museum is Levent Ã‡alÄ±koglu, and the chair of the board of directors is Oya EczacÄ±baÅŸÄ±.', 'http://angelshomehotel.com/wp-content/uploads/2014/07/istanbul-modern-2.jpg', 2, 2),
                           ('Zöhre Ustanın Yeri', 'A perfect dinner place. It has fixed prices for breakfasts and dinners. Tea is free', 'https://scontent-frt3-1.xx.fbcdn.net/v/t1.0-9/12936641_116577862075997_6646060229600396520_n.jpg?oh=8f8770a4d7aca61a3dad9a4a7c2dd1cb&oe=58B4EFD6', 3, 5),
                           ('Sükrü Saraçoğlu Stadı', 'The Sükrü Saraçoğlu Stadium, also officially known as Ülker Stadium Fenerbahçe Şükrü Saraçoğlu Sports Complex or simply Ülker Stadium due to sponsorship reasons, is a football stadium in Kadıköy, İstanbul, Turkey, and is the home venue of Fenerbahçe S.K. It was inaugurated in 1908 and renovated between 1929 and 1932, 1965 and 1982, and 1999 and 2006. On October 4, 2006, after numerous inspections by UEFA, Fenerbahçe Şükrü Saraçoğlu Stadium was selected to host the 2009 UEFA Cup Final that went down to history as the last Final of the UEFA Cup football tournament, which was replaced by the UEFA Europa League starting from the 2009-2010 season.', 'https://fys.tff.org/TFFUploadFolder/StadResimleri/3402/6.jpg', 2, 1),
                           ('Cemil Topuzlu Open-Air Theatre', 'The Cemil Topuzlu Open-Air Theatre (Turkish: Cemil Topuzlu Harbiye Açık Hava Tiyatrosu, also called simply Açık Hava Tiyatrosu) is a contemporary amphitheatre located at Harbiye neighborhood of Şişli district in Istanbul, Turkey. It is situated across from the Istanbul Lütfi Kırdar Convention and Exhibition Center, and behind the Hilton Istanbul Bosphorus on the European side of the city.', 'http://www.buldumbuldum.com/blog/wp-content/uploads/2014/05/anneler-gununu-aktivitelere-bogmak-ister-misiniz-6.jpg', 2, 4),
                           ('Cazgır Cafe', 'Most crovded and biggest cafe of Uzunkopru. It has a good landscape. A litle bit expensive. But its landscape neutrolizes it', 'http://www.uzunkoprutb.org.tr/uploads/gallery/DU2aQ/20022014OFkvpM.JPG', 4, 6),
                           ('Golden Bridge', 'The Golden Gate Bridge is a suspension bridge spanning the Golden Gate strait, the one-mile-wide (1.6 km), three-mile-long (4.8 km) channel between San Francisco Bay and the Pacific Ocean. The structure links the American city of San Francisco, California â€“ the northern tip of the San Francisco Peninsula â€“ to Marin County, carrying both U.S. Route 101 and California State Route 1 across the strait. The bridge is one of the most internationally recognized symbols of San Francisco, California, and the United States. It has been declared one of the Wonders of the Modern World by the American Society of Civil Engineers.', 'https://images.indiegogo.com/file_attachments/993310/files/20141106235403-golden-gate-bridge.jpg?1415346843', 4, 7)
                           """
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS Transportation"""
        cursor.execute(query)

        query = """CREATE TABLE Transportation(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                INFO TEXT,
                PHOTO VARCHAR(255) DEFAULT 'https://cdn3.iconfinder.com/data/icons/glypho-movie-and-video/64/theater-masks-512.png',
                PLACE INTEGER REFERENCES Location (ID) ON DELETE CASCADE
                )"""
        cursor.execute(query)

        query = """INSERT INTO Transportation(NAME,INFO,PHOTO,PLACE)
                    VALUES ('Büyük İstanbul Otogarı', 'Esenler Bus Terminus (Turkish: Esenler Otogarı), is the central and largest bus terminus for intercity bus service in İstanbul, Turkey. Although the terminus is located in Bayrampaşa district it is named after Esenler district, which is closer.', 'http://i.milliyet.com.tr/YeniAnaResim/2016/04/23/fft99_mf6921598.Jpeg', 9),
                           ('Ankara Esenboğa Airport', 'Esenboğa International Airport (IATA: ESB, ICAO: LTAC) (Turkish: Ankara Esenboğa Havalimanı or Esenboğa Uluslararası Havalimanı), is the international airport of Ankara, the capital city of Turkey. It has been operating since 1955. In 2014, the airport has served more than 11 million passengers in total, 4.9 million of which were domestic passengers. It ranked 4th in terms of total passenger traffic (after Ataturk Airport, Antalya Airport and Sabiha Gökçen Airport), 3rd in terms of domestic passenger traffic (after Ataturk Airport and Sabiha Gökçen Airport) among airports in Turkey', 'http://www.esenbogaairport.com//tr-TR/Lists/PressRelease/Attachments/44/Ankara_Esenboga.jpg', 12),
                           ('İstanbul Atatürk Airport', 'Istanbul Atatürk Airport (IATA: IST, ICAO: LTBA) (Turkish: İstanbul Atatürk Havalimanı) is the main international airport serving Istanbul, and the biggest airport in Turkey by total number of passengers, destinations served and aircraft movements. Opened in 1924 in Yeşilköy, on the European side of the city, it is located 24 km (15 mi) west[2] of the city centre and serves as the main hub for Turkish Airlines. The citys other smaller international airport is Sabiha Gökçen International Airport.', 'http://www.ataturkairport.com//AHLPictureGalery/ist_ataturk_08_0116_2.jpg', 10),
                           ('Sabiha Gökçen International Airport', 'Sabiha Gökçen International Airport (IATA: SAW, ICAO: LTFJ) is one of the two international airports serving İstanbul, the largest city in Turkey, the other being Atatürk Airport. Located 35 km (22 mi) southeast[1] of central İstanbul, Sabiha Gökçen is on the Asian side of the bi-continental city and serves as the hub for Pegasus Airlines as well as a base for Turkish Airlines and Borajet. The facility is named after Sabiha Gökçen, the first female combat pilot in Turkey.', 'http://www.istanbulhotels.in/UserFiles/ArticleFiles/sabiha-gokcen-international-airport18434019.jpg', 11)"""

        cursor.execute(query)

        ##################################################################

        query = """DROP TABLE IF EXISTS PEOPLE CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE PEOPLE (
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
                )"""
        cursor.execute(query)

        query = """INSERT INTO PEOPLE (NAME, SURNAME, USERNAME, PASSWORD, EMAIL, AGE, WHENCE_ID, PHOTO, BEST_ACTIVITY_ID, BEST_PLACE_ID, BEST_CULTURE_ID)
                    VALUES ('Fatih', 'Budak ', 'budakf', '123456789', 'email of budakf ', 24, 2, 'http://previews.123rf.com/images/richcat/richcat1109/richcat110900082/10732608-Graphic-illustration-of-man-in-business-suit-as-user-icon-avatar-Stock-Vector.jpg', 1, 1, 1),
                           ('Güray', 'Ocak ', 'ocakg', '123456789','email of ocakg ', 24, 2, 'https://pbs.twimg.com/profile_images/710169276980858880/eosxkWG0.jpg', 3, 2, 3),
                           ('Mehmet', 'Ozen ', 'tozen', '123456789','email of tozen ', 23, 3,'http://i3.mirror.co.uk/incoming/article9325019.ece/ALTERNATES/s482b/Steven-Gerrard-teaser.jpg', 4, 4, 1),
                           ('Berkan', 'Dinar ', 'dinar', '123456789','email of dinar ', 22, 4,'http://previews.123rf.com/images/richcat/richcat1109/richcat110900082/10732608-Graphic-illustration-of-man-in-business-suit-as-user-icon-avatar-Stock-Vector.jpg', 2, 3, 2)"""
        cursor.execute(query)

            ###########

        query = """DROP TABLE IF EXISTS LANDMARK CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE LANDMARK (
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                PHOTO VARCHAR(255),
                LOCATIONID INTEGER REFERENCES Cities(ID) ON DELETE CASCADE,
                VOTES INTEGER DEFAULT 0,
                INFO TEXT
                )"""
        cursor.execute(query)

        query = """INSERT INTO LANDMARK (NAME, PHOTO, LOCATIONID, INFO)
                    VALUES ('Maiden Tower ', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTeO96yh3Q0CsmzyLGBGXpscCP5oLsM1HVxpVATlXy09o3dTNWD', 6,
                            'The Maiden Tower also known as Leander s Tower (Tower of Leandros) since the medieval Byzantine period, is a tower lying on a small islet located at the southern entrance of the Bosphorus strait 200 m (220 yd) from the coast of Usküdar in Istanbul, Turkey.After the naval victory at Cyzicus, the ancient Athenian general Alcibiades possibly built a custom station for ships coming from the Black Sea on a small rock in front of Chrysopolis (today s Usküdar).[2] In 1110 Byzantine Emperor Alexius Comnenus built a wooden tower protected by a stone wall.[2] From the tower an iron chain stretched across to another tower erected on the European shore, at the quarter of Mangana in Constantinople.[2] The islet was then connected to the Asiatic shore through a defense wall, whose underwater remains are still visible.[2] During the Ottoman conquest of Constantinople (Istanbul) in 1453, the tower held a Byzantine garrison commanded by the Venetian Gabriele Trevisano.[2] Subsequently, the structure was used as a watchtower by the Ottoman Turks during the reign of Sultan Mehmed the Conqueror.' ),
                           ('Statue of Liberty ','https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSbk4vnRjWyAGgU7GMxVl3VNjGoSIIYb7jDAuYhEu-VyiqBJgCvEg', 7,
                           'The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in New York City, in the United States. The copper statue, designed by Frederic Auguste Bartholdi, a French sculptor, was built by Gustave Eiffel and dedicated on October 28, 1886. It was a gift to the United States from the people of France. The statue is of a robed female figure representing Libertas, the Roman goddess, who bears a torch and a tabula ansata (a tablet evoking the law) upon which is inscribed the date of the American Declaration of Independence, July 4, 1776. A broken chain lies at her feet. The statue is an icon of freedom and of the United States, and was a welcoming sight to immigrants arriving from abroad.'),
                           ('Leaning Tower of Pisa ','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-I2xUehvjKzrUF5yJKsw-9NEIOrjTwfuAdDfNtQep8jI2wrYj', 8,
                           'The Leaning Tower of Pisa (Italian: Torre pendente di Pisa) or simply the Tower of Pisa  is the campanile, or freestanding bell tower, of the cathedral of the Italian city of Pisa, known worldwide for its unintended tilt. It is situated behind Pisa s cathedral and is the third oldest structure in the city s Cathedral Square (Piazza del Duomo) after the cathedral and the Pisa Baptistry. The tower s tilt began during construction, caused by an inadequate foundation on ground too soft on one side to properly support the structure s weight. The tilt increased in the decades before the structure was completed, and gradually increased until the structure was stabilized (and the tilt partially corrected) by efforts in the late 20th and early 21st centuries. The height of the tower is 55.86 metres (183.27 feet) from the ground on the low side and 56.67 metres (185.93 feet) on the high side. The width of the walls at the base is 2.44 m (8 ft 0.06 in). Its weight is estimated at 14,500 metric tons (16,000 short tons).[1] The tower has 296 or 294 steps; the seventh floor has two fewer steps on the north-facing staircase. Prior to restoration work performed between 1990 and 2001, the tower leaned at an angle of 5.5 degrees,[2][3][4] but the tower now leans at about 3.99 degrees.[5] This means that the top of the tower is displaced horizontally 3.9 metres (12 ft 10 in) from the centre.'),
                           ('Christ the Redeemer ','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK88g7zwwUpvrqn6DEHysSdPouU4iuRpNZ8HQtoTTsAhf9nvSo', 9,
                           'Christ the Redeemer (Portuguese: Cristo Redentor is an Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil, created by French sculptor Paul Landowski and built by the Brazilian engineer Heitor da Silva Costa, in collaboration with the French engineer Albert Caquot. Romanian sculptor Gheorghe Leonida fashioned the face. The statue is 30 metres (98 ft) tall, not including its 8-metre (26 ft) pedestal, and its arms stretch 28 metres (92 ft) wide. The statue weighs 635 metric tons (625 long, 700 short tons), and is located at the peak of the 700-metre (2,300 ft) Corcovado mountain in the Tijuca Forest National Park overlooking the city of Rio. A symbol of Christianity across the world, the statue has also become a cultural icon of both Rio de Janeiro and Brazil, and is listed as one of the New Seven Wonders of the World.[3] It is made of reinforced concrete and soapstone, and was constructed between 1922 and 1931.')"""
        cursor.execute(query)

            ##################################################################
        query = """DROP TABLE IF EXISTS AGENCY CASCADE"""
        cursor.execute(query)

        query = """CREATE TABLE AGENCY(
                ID SERIAL PRIMARY KEY,
                NAME VARCHAR(255) NOT NULL,
                SCORE SCORES DEFAULT 0,
                PHOTO VARCHAR(255),
                VOTES INTEGER DEFAULT 0,
                INFO TEXT
                )"""
        cursor.execute(query)

        query = """INSERT INTO AGENCY (NAME, PHOTO, INFO)
                VALUES('STA Travel','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVz6MfrguKy_uhS4mxObQzAtMtgNdAi7udJNsQ1IhR3Wp0aS3I', 'http://www.statravel.co.uk/'),
                    ('Star Tours','https://s23.postimg.org/mc3zr75wn/star.png','http://www.startours.co.uk/'),
                    ('Insight Vacations','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJ8n4SWkqSZQM6OOhY09RrZycG-geMf7xUhAiQipKSoMp959ks','https://www.insightvacations.com/eu'),
                    ('Tucan Travel','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ8ZxcD0g0FYg4hrPAYexzFJCugurotFP0ZjnNXpO1qtB7tYj42Dg','https://www.tucantravel.com/')
                    """
        cursor.execute(query)
            ##################################################################

        connection.commit()
    return redirect(url_for('home_page'))

@app.route('/login', methods=['GET','POST'])
def login_page():
    T=True
    id=1
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('home_page'))

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
                                cursor.execute(statement, (T,id ) )
                                return redirect(url_for('home_page'))

    return render_template('login.html')

@app.route('/logout')
def logout_page():
    T=False
    session.pop('user', None)
    with dbapi2.connect(app.config['dsn']) as connection:
        with connection.cursor() as cursor:
            statement = """UPDATE PEOPLE SET (ISACTIVE) = (%s) """
            cursor.execute(statement, (T, ) )
    return redirect(url_for('home_page'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

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

