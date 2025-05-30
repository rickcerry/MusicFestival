from dbPackage import DATABASE
import sqlite3

# Designed for Stages table 

# Get all stages
def getStages():
    sql = "SELECT * FROM Stages"
  
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)

    stages = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return stages

# Given an ID, returns the ticket type
def getStage(id):
    sql = "SELECT * FROM Stages WHERE Stages.ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    
    stage = cursor.fetchone()

    cursor.close()
    conn.close()

    return stage