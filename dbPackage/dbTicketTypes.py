from dbPackage import DATABASE
import sqlite3

# Designed for TicketTypes table 

# Get all ticket types
def getTicketTypes():
    sql = "SELECT * FROM TicketTypes"
  
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)

    ticketTypes = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return ticketTypes

# Given an ID, returns the ticket type
def getTicketType(id):
    sql = "SELECT * FROM TicketTypes WHERE TicketTypes.ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    
    ticketType = cursor.fetchone()

    cursor.close()
    conn.close()

    return ticketType

# Returns the number of ticket types
def getNoTicketTypes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT COUNT(*)
            FROM TicketTypes
        """)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count