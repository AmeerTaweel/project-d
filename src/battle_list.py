from bottle import template

def battle_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT R1.*, R2.*, D1.Name, D2.Name, C.Name
        FROM Records AS R1, Drivers AS D1, Records AS R2, Drivers AS D2, Courses AS C
        WHERE R1.ID > R2.ID
        AND R1.DriverID = D1.ID
        AND R2.DriverID = D2.ID
        AND R1.CourseID = C.ID
        AND R1.BattleID = R2.BattleID
        AND R1.BattleID IS NOT NULL
        ORDER BY R1.Date DESC
        LIMIT 100
    """)

    battles = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("battle-list", battles = battles)
