from bottle import template, abort

def driver_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT D.*, T.Name
        FROM Drivers AS D LEFT OUTER JOIN Teams AS T
        ON D.TeamID = T.ID
        WHERE D.ID = {id}
    """)

    drivers = tuple(row for row in db_cursor)

    if len(drivers) != 1:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    driver = drivers[0]

    db_cursor.execute(f"""
        SELECT COUNT(IF(R1Min < R2Min, 1, NULL)),
               COUNT(IF(R1Min = R2Min, 1, NULL)),
               COUNT(IF(R1Min > R2Min, 1, NULL))
        FROM (
            SELECT R1.BattleID AS BID, D1.ID AS D1ID, D1.Name AS D1Name, D2.ID
                   AS D2ID, D2.Name AS D2Name, R1.Minutes AS R1Min,
                   R2.Minutes AS R2Min, R1.Date AS Date
            FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2
            WHERE R1.ID <> R2.ID
            AND D1.ID = R1.DriverID
            AND D2.ID = R2.DriverID
            AND D1.ID = {id}
            AND R1.BattleID = R2.BattleID
            AND R1.BattleID IS NOT NULL
        ) AS X
    """)

    wdl = tuple(row for row in db_cursor)[0]

    db_cursor.execute(f"""
        SELECT R.ID, C.ID, C.Name, R.Minutes, R.Date
        FROM Records AS R, Courses AS C
        WHERE R.DriverID = {id}
        AND R.CourseID = C.ID
        AND (C.ID, R.Minutes) IN (
            SELECT DISTINCT CourseID, MIN(Minutes)
            FROM Records
            WHERE DriverID = {id}
            GROUP BY CourseID
        )
        ORDER BY C.ID ASC
    """)

    top_records = [row for row in db_cursor]

    db_cursor.execute(f"""
        SELECT R.ID, C.ID, C.Name, R.Minutes, R.Date
        FROM Records AS R, Courses AS C
        WHERE R.DriverID = {id}
        AND R.CourseID = C.ID
        ORDER BY R.Date DESC
    """)

    all_records = [row for row in db_cursor]

    db_cursor.execute(f"""
        SELECT R1.BattleID, D.ID, D.Name, C.ID, C.Name, R1.Minutes, R2.Minutes, R1.Date
        FROM Drivers AS D, Courses AS C, Records AS R1, Records AS R2
        WHERE R1.ID <> R2.ID
        AND R1.DriverID = {id}
        AND D.ID = R2.DriverID
        AND R1.BattleID = R2.BattleID
        AND R1.BattleID IS NOT NULL
        AND R1.CourseID = C.ID
        ORDER BY R1.Date DESC
    """)

    all_battles = [row for row in db_cursor]

    team_id = driver[3]

    all_team_battles = ()

    if team_id != None:
        db_cursor.execute(f"""
            SELECT X.TeamBattleID AS TBID, X.Date AS Date,
            C.ID, C.Name, X.TeamID, X.TeamName,
            COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
            COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
            FROM (
                SELECT B.TeamBattleID AS TeamBAttleID,
                       B.ID AS BattleID,
                       R1.Minutes AS Min1,
                       R2.Minutes AS Min2,
                       R1.CourseID AS CourseID,
                       R1.Date AS Date,
                       T2.ID AS TeamID,
                       T2.Name AS TeamName
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
                AND T1.ID = {team_id}
                AND D2.TeamID = T2.ID
            ) AS X, Courses AS C
            WHERE X.CourseID = C.ID
            AND X.TeamBattleID IN (
                SELECT TeamBattles.ID
                FROM Records, Battles, TeamBattles
                WHERE Records.BattleID = Battles.ID
                AND Battles.TeamBattleID = TeamBattles.ID
                AND Records.DriverID = {id}
            )
            GROUP BY TBID
            ORDER BY Date DESC
        """)

        all_team_battles = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "driver-info",
        driver = driver,
        wdl = wdl,
        top_records = top_records,
        all_records = all_records,
        all_battles = all_battles,
        all_team_battles = all_team_battles
    )
