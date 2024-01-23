from bottle import template, abort

def record_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT R.*, D.Name, C.Name
        FROM Records AS R, Drivers AS D, Courses AS C
        WHERE R.ID = {id}
        AND R.DriverID = D.ID
        AND R.CourseID = C.ID
    """)

    records = tuple(row for row in db_cursor)

    if len(records) != 1:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    record = records[0]

    battle_id = record[5]

    team_battle_id = None

    if battle_id != None:
        db_cursor.execute(f"""
            SELECT TeamBattleID
            FROM Battles
            WHERE ID = {battle_id}
        """)

        team_battle_id = tuple(row for row in db_cursor)[0][0]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "record-info",
        record = record,
        team_battle_id = team_battle_id
    )
