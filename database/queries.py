import mysql.connector
import connectors as cn

db = mysql.connector.connect(
    host=cn.host,
    user=cn.user,
    passwd=cn.passwd,
    database=cn.database
)

mycursor = db.cursor()

# mycursor.execute("CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(50))")
# mycursor.execute("DESCRIBE User")

# mycursor.execute("INSERT INTO User (username, password) VALUES (%s, %s)", ("dutz", "1234"))
# db.commit()

mycursor.execute("SELECT * FROM User")

for elem in mycursor:
    print(elem)
