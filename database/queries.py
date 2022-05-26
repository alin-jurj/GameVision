import mysql.connector
import database.connectors as cn

db = mysql.connector.connect(
    host=cn.host,
    user=cn.user,
    passwd=cn.passwd,
    database=cn.database
)

mycursor = db.cursor()


def logs(input_box1, input_box2):
    mycursor.execute("SELECT * FROM User WHERE username=%s AND password=%s",
                     (input_box1.get_text(), input_box2.get_text()))
    row = mycursor.fetchone()
    return row


def search_username(username_field):
    mycursor.execute("SELECT * FROM User WHERE username=%s", (username_field.get_text(),))
    row = mycursor.fetchone()
    return row


def search_email(email_field):
    mycursor.execute("SELECT * FROM User WHERE email=%s", (email_field.get_text(),))
    row = mycursor.fetchone()
    return row


def add_user(username_field, password_field, email_field):
    mycursor.execute(
        "INSERT INTO User (username, password, email, wins, losses, lvl, xp) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (username_field.get_text(), password_field.get_text(), email_field.get_text(), 0, 0, 1, 0))
    db.commit()


def add_champion(userId, championId):
    mycursor.execute(
        "INSERT INTO User_Champions (userId, championId) VALUES (%s, %s)",
        (userId, championId)
    )
    db.commit()


def select_random_champion(userId):
    mycursor.execute(
        "SELECT championName, hp, attack, defense, energy, price FROM champion "
        "WHERE championId NOT IN "
        "(SELECT championId FROM user_champions "
        "WHERE userId=%s) "
        "AND price IS NOT NULL "
        "ORDER BY RAND() "
        "LIMIT 1", (userId,)
    )
    row = mycursor.fetchone()
    return row


def get_owned_champions(userId):
    mycursor.execute(
        "SELECT champion.championId, championName "
        "FROM champion "
        "JOIN user_champions ON champion.championId = user_champions.championId "
        "JOIN user ON user.userId = user_champions.userId "
        "WHERE user.userId = %s", (userId,)
    )
    row = mycursor.fetchall()
    return row


def all_ordered_users_by_win_rate():
    mycursor.execute("SELECT * FROM User ORDER BY wins/(wins+losses) DESC, wins DESC")
    row = mycursor.fetchall()
    return row


def delete_table():
    mycursor.execute("DROP TABLE User")
    db.commit()


def create_table():
    mycursor.execute(
        "CREATE TABLE User_Champions (userId int NOT NULL, championId int NOT NULL,"
        "FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE CASCADE ON UPDATE CASCADE,"
        "FOREIGN KEY (championId) REFERENCES Champion (championId) ON DELETE CASCADE ON UPDATE CASCADE,"
        "PRIMARY KEY (userId, championId))"
    )

# "CREATE TABLE User_Champions (userId int NOT NULL, championId int NOT NULL,"
# "FOREIGN KEY (userId) REFERENCES User (userId) ON DELETE RESTRICT ON UPDATE CASCADE,"
# "FOREIGN KEY (championId) REFERENCES Champion (championId) ON DELETE RESTRICT ON UPDATE CASCADE,"
# "PRIMARY KEY (userId, championId))"

# "CREATE TABLE Champion (championId int PRIMARY KEY AUTO_INCREMENT NOT NULL, championName VARCHAR(12) NOT NULL,"
# " hp INT(7) NOT NULL, attack INT(7) NOT NULL, defense INT(7) NOT NULL, energy INT(7) NOT NULL, price INT(7))"

# "CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT NOT NULL, "
# "username VARCHAR(13) NOT NULL, password VARCHAR(50) NOT NULL, "
# "email VARCHAR(50) NOT NULL, wins INT(7) DEFAULT 0, losses INT(7) DEFAULT 0, "
# "lvl INT(7) DEFAULT 1, xp INT(7) DEFAULT 0, money INT DEFAULT 0)"

#"CREATE TABLE Champion (characterId int PRIMARY KEY AUTO_INCREMENT, hp INT(7), attack INT(7), defense INT(7), energy INT(7), price INT(7))")
# "CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(13), password VARCHAR(50), email VARCHAR(50), wins INT(7), losses INT(7), lvl INT(7), xp INT(7))"

# mycursor.execute("CREATE DATABASE testdatabase")
# mycursor.execute("CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(50))")
# mycursor.execute("DESCRIBE User")

# mycursor.execute("INSERT INTO User (username, password, email) VALUES (%s, %s, %s)", ("alin", "1234","alin_jurj@yahoo.com"))
# db.commit()

# mycursor.execute("SELECT * FROM User")

# for elem in mycursor:
#    print(elem)
