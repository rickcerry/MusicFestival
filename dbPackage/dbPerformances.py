from dbPackage import DATABASE
import sqlite3

def getPerformance(performance_id):
    sql = "SELECT * FROM Performances WHERE Performances.ID = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (performance_id,))
    
    performance = cursor.fetchone()

    cursor.close()
    conn.close()

    return performance

def addPerformance(artist, genre, description, promotional_image, organizer_id, start_day, start_hour, end_day, end_hour, stage_id):
    
    sql = "INSERT INTO Performances (ArtistName, Genre, Description, PromotionalImage, Organizer_ID, Published, StartDay_ID, StartHour, EndDay_ID, EndHour, Stage_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (artist, genre, description, promotional_image, organizer_id, 0, start_day, start_hour, end_day, end_hour, stage_id))
    
    conn.commit()
    
    cursor.close()
    conn.close()
    

def publishPerformance(performance_id):
    sql = """
    UPDATE Performances
    SET Published = 1
    WHERE Performances.ID = ?;
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sql, (performance_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
          
def isArtistPresent(artist_id):
    sql = "SELECT * FROM Performances WHERE Performances.ArtistName = ?"

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql, (artist_id,))
    
    exists = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return exists

          

def isPerformanceAddable(performance_id):
    
          performance_compare = getPerformance(performance_id)
          stage_id = performance_compare["Stage_ID"]
          start_day = performance_compare["StartDay_ID"]
          start_hour = performance_compare["StartHour"]
          end_day = performance_compare["EndDay_ID"]
          end_hour = performance_compare["EndHour"]
          
          sql = """
          SELECT COUNT(*)
          FROM Performances
          WHERE Published = 1
          AND Stage_ID = ?
          AND (
          (? < EndDay_ID OR (? = EndDay_ID AND ? < EndHour))
          AND
          (? > StartDay_ID OR (? = StartDay_ID AND ? > StartHour))
          );
          """
          
          conn = sqlite3.connect(DATABASE)
          conn.row_factory = sqlite3.Row
          cursor = conn.cursor()
          cursor.execute(sql, (stage_id, start_day, start_day, start_hour, end_day, end_day, end_hour))

          overlap_count = cursor.fetchone()[0]

          cursor.close()
          conn.close()

          if overlap_count == 0:
                    return True
          else:
                    return False

# Returns the number of performances
def getNoPerformances():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT COUNT(*)
            FROM Performances
            WHERE Performances.Published = 1
        """)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def getDraftPerformancesByID(id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT *
            FROM Performances
            WHERE Performances.Organizer_ID = ?
            AND Performances.Published = 0
        """, (id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def clearPerformances():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM Performances")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='Performances'")
    
    conn.commit()
    cursor.close()
    conn.close()
    
def getPublishedPerformances():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
            SELECT *
            FROM Performances
            WHERE Performances.Published = 1
        """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results