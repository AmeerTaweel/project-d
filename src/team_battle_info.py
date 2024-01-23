from bottle import template, abort

def team_battle_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT B.TeamBattleID, B.ID,
               R1.Minutes, R2.Minutes,
               C.ID, C.Name, R1.Date,
               T1.ID, T1.Name, T2.ID, T2.Name,
               D1.ID, D1.Name, D2.ID, D2.Name
        FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
             Battles AS B, Teams AS T1, Teams AS T2, Courses AS C
        WHERE R1.ID <> R2.ID
        AND D1.ID = R1.DriverID
        AND D2.ID = R2.DriverID
        AND R1.BattleID = R2.BattleID
        AND R1.BattleID IS NOT NULL
        AND R2.BattleID = B.ID
        AND B.TeamBattleID IS NOT NULL
        AND D1.TeamID = T1.ID
        AND D2.TeamID = T2.ID
        AND T1.ID > T2.ID
        AND B.TeamBattleID = {id}
        AND R1.CourseID = C.ID
        ORDER BY B.ID ASC
    """)

    battles = tuple(row for row in db_cursor)

    if len(battles) == 0:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "team-battle-info",
        battles = battles
    )
