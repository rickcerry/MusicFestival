from . import DATABASE
import sqlite3

def insertDay(day, format, noPeople):
    sql = "INSERT INTO Days (Day, YYYY_MM_DD, NoPeople) VALUES (?, ?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (day, format, noPeople))

    conn.commit()
    
    cursor.close()
    conn.close()
    
def getDays():
    sql = "SELECT * FROM Days"
  
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)

    days = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return days

def getNoDays():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT COUNT(*)
            FROM Days
        """)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def clearDays():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Days")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Days'")
    
    conn.commit()
    cursor.close()
    conn.close()