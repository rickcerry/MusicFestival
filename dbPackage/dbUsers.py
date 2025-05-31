from dbPackage import DATABASE
import sqlite3

# Designed for Users table 

# Inserts a user
def insertUser(name, surname, email, typeUser, password):
    success = False
    sql = "INSERT INTO Users (Name, Surname, EMail, Type, Password) VALUES (?, ?, ?, ?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, (name, surname, email, typeUser, password))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

# Given an ID, returns the user
def getUser(id):
    sql = "SELECT * FROM Users WHERE Users.ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

def getUserViaEmail(email):
    sql = "SELECT * FROM Users WHERE Users.EMail = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (email,))
    
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# Get all users
def getUsers():
    sql = "SELECT * FROM Users"
  
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)

    users = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return users

def clearUsers():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Users")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Users'")

    
    conn.commit()
    cursor.close()
    conn.close()