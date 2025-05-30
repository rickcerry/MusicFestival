from dbPackage import DATABASE
import sqlite3

def insertDay(day, format):
    sql = "INSERT INTO Days (Day, YYYY_MM_GG) VALUES (?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (day, format))
    
    conn.commit()
    
    cursor.close()
    conn.close()

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