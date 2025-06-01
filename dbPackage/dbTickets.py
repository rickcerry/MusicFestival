from dbPackage import DATABASE
import sqlite3

MAX_TICKETS_DAILY = 200

# Designed for Tickets table 

def hasIDTicket(person_id):
    sql = "SELECT * FROM Tickets WHERE Tickets.Customer_ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (person_id,))
    
    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists

# Insert ticket in DB
def insertTicket(ticket_type, start_day, end_day, customer_id):
    sql = "INSERT INTO Tickets (TicketType_ID, StartDay_ID, EndDay_ID, Customer_ID) VALUES (?, ?, ?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (ticket_type, start_day, end_day, customer_id))
    
    conn.commit()
    
    cursor.close()
    conn.close()

# Get all tickets
def getTickets():
    sql = "SELECT * FROM Tickets"
  
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)

    tickets = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return tickets

# Given an ID, returns the ticket
def getTicketType(id):
    sql = "SELECT * FROM Tickets WHERE Tickets.ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    
    ticket = cursor.fetchone()

    cursor.close()
    conn.close()

    return ticket

def isTicketAddable(start_day, end_day):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    for day in range(start_day, end_day + 1):
        cursor.execute("""
            SELECT COUNT(*)
            FROM Tickets
            WHERE StartDay_ID <= ? AND EndDay_ID >= ?
        """, (day, day))
        count = cursor.fetchone()[0]
        if count >= MAX_TICKETS_DAILY:
            cursor.close()
            conn.close()
            return False
    
    cursor.close()
    conn.close()
    return True

# Returns the number of tickets
def getNoTickets():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT COUNT(*)
            FROM Tickets
        """)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def clearDays():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Tickets")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Tickets'")
    
    conn.commit()
    cursor.close()
    conn.close()