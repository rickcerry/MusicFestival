from dbPackage import DATABASE
import sqlite3

def publishPerformance(performance_id):
          sql = """
          UPDATE Performances
          SET Published = 1
          WHERE CustomerID = ?;
          """
          conn = sqlite3.connect(DATABASE)
          cursor = conn.cursor()
          cursor.execute(sql, (performance_id,))
          
          conn.commit()
          
          cursor.close()
          conn.close()
          

def isPerformanceAddable(stage_id, start_day, start_hour, end_day, end_hour):
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
        """)
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count