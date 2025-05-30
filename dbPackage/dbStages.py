from dbPackage import DATABASE
import sqlite3

# Designed for Stages table 

def insertStage(primary, secondary):
    sql = "INSERT INTO Stages (PrimaryName, SecondaryName) VALUES (?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (primary, secondary))
    
    conn.commit()
    
    cursor.close()
    conn.close()

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

def clearStages():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Stages")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Stages'")

    
    conn.commit()
    cursor.close()
    conn.close()