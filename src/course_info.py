from bottle import template, abort

def course_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"SELECT * FROM Courses WHERE ID = {id}")

    courses = tuple(row for row in db_cursor)

    if len(courses) != 1:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    course = courses[0]

    db_cursor.execute(f"""
        SELECT R.ID, D.ID, D.Name, R.Minutes, R.Date
        FROM Drivers AS D, Records AS R
        WHERE D.ID = R.DriverID
        AND R.CourseID = {id}
        ORDER BY R.Minutes ASC, R.Date DESC
        LIMIT 3
    """)

    top_records = [row for row in db_cursor]

    db_cursor.execute(f"""
        SELECT R.ID, D.ID, D.Name, R.Minutes, R.Date
        FROM Drivers AS D, Records AS R
        WHERE D.ID = R.DriverID
        AND R.CourseID = {id}
        ORDER BY R.Date DESC
    """)

    all_records = [row for row in db_cursor]

    db_cursor.execute(f"""
        SELECT R1.BattleID, D1.ID, D1.Name, D2.ID, D2.Name, R1.Minutes, R2.Minutes, R1.Date
        FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2
        WHERE R1.ID > R2.ID
        AND D1.ID = R1.DriverID
        AND D2.ID = R2.DriverID
        AND R1.BattleID = R2.BattleID
        AND R1.BattleID IS NOT NULL
        AND R1.CourseID = {id}
        ORDER BY R1.Date DESC
    """)

    all_battles = [row for row in db_cursor]

    db_cursor.execute(f"""
        SELECT X.TeamBattleID AS TBID, X.Date AS Date,
        X.TID1, X.TName1, X.TID2, X.TName2,
        COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
        COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
        FROM (
            SELECT B.TeamBattleID AS TeamBAttleID,
                   B.ID AS BattleID,
                   R1.Minutes AS Min1,
                   R2.Minutes AS Min2,
                   R1.CourseID AS CourseID,
                   R1.Date AS Date,
                   T1.ID AS TID1,
                   T1.Name AS TName1,
                   T2.ID AS TID2,
                   T2.Name AS TName2
            FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                 Battles AS B, Teams AS T1, Teams AS T2
            WHERE R1.ID <> R2.ID
            AND D1.ID = R1.DriverID
            AND D2.ID = R2.DriverID
            AND R1.BattleID = R2.BattleID
            AND R1.BattleID IS NOT NULL
            AND R2.BattleID = B.ID
            AND B.TeamBattleID IS NOT NULL
            AND R1.Minutes <> R2.Minutes
            AND D1.TeamID = T1.ID
            AND D2.TeamID = T2.ID
            AND T1.ID > T2.ID
            AND R1.CourseID = {id}
        ) AS X
        GROUP BY TBID
        ORDER BY Date DESC
    """)

    all_team_battles = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "course-info",
        course = course,
        top_records = top_records,
        all_records = all_records,
        all_battles = all_battles,
        all_team_battles = all_team_battles
    )
