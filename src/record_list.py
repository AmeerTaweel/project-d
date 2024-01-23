from bottle import template

def record_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT R.*, D.Name, C.Name
        FROM Records AS R, Drivers AS D, Courses AS C
        WHERE R.DriverID = D.ID
        AND R.CourseID = C.ID
        ORDER BY R.Date DESC
        LIMIT 100
    """)

    records = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("record-list", records = records)
