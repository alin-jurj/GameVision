import mysql.connector
import database.connectors as cn


db = mysql.connector.connect(
    host=cn.host,
    user=cn.user,
    passwd=cn.passwd,
    database=cn.database
)

mycursor = db.cursor()

def logs(input_box1,input_box2):
    mycursor.execute("SELECT * FROM User WHERE username=%s AND password=%s",(input_box1.get_text(), input_box2.get_text()))
    row = mycursor.fetchone()
    return row
def search_username(username_field):
    mycursor.execute("SELECT * FROM User WHERE username=%s",(username_field.get_text(),))
    row = mycursor.fetchone()
    return row
def search_email(email_field):
    mycursor.execute("SELECT * FROM User WHERE email=%s",(email_field.get_text(),))
    row = mycursor.fetchone()
    return row

def add_user(username_field, password_field,email_field):
    mycursor.execute("INSERT INTO User (username, password, email, wins, losses, lvl, xp) VALUES (%s, %s,%s, %s, %s, %s, %s)", (username_field.get_text(), password_field.get_text(),email_field.get_text(),0,3,1,0))
    db.commit()
def all_ordered_users_by_win_rate():
    mycursor.execute("SELECT * FROM User ORDER BY wins/(wins+losses) DESC, wins DESC")
    row = mycursor.fetchall()
    return row
def delete_table():
    mycursor.execute("DROP TABLE User")
    db.commit()
def create_table():
    mycursor.execute("CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(13), password VARCHAR(50), email VARCHAR(50), wins INT(7), losses INT(7), lvl INT(7), xp INT(7))")
#mycursor.execute("CREATE DATABASE testdatabase")
#mycursor.execute("CREATE TABLE User (userId int PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(50))")
#mycursor.execute("DESCRIBE User")

#mycursor.execute("INSERT INTO User (username, password, email) VALUES (%s, %s, %s)", ("alin", "1234","alin_jurj@yahoo.com"))
#db.commit()

#mycursor.execute("SELECT * FROM User")

#for elem in mycursor:
#    print(elem)
