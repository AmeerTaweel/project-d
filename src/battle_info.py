from bottle import template, abort

def battle_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT R1.*, R2.*, D1.Name, D2.Name, C.Name, B.TeamBattleID
        FROM Records AS R1, Drivers AS D1, Records AS R2, Drivers AS D2,
             Courses AS C, Battles AS B
        WHERE R1.ID > R2.ID
        AND R1.DriverID = D1.ID
        AND R2.DriverID = D2.ID
        AND R1.CourseID = C.ID
        AND R1.BattleID = R2.BattleID
        AND R1.BattleID = {id}
        AND R1.BattleID = B.ID
    """)

    battles = tuple(row for row in db_cursor)

    if len(battles) != 1:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    battle = battles[0]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "battle-info",
        battle = battle
    )
