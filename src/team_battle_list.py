from bottle import template

def team_battle_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT X.TeamBattleID AS TBID, X.Date AS Date,
        X.TID1, X.TName1, X.TID2, X.TName2, C.ID, C.Name,
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
            AND B.TeamBattleID > (
                SELECT MAX(ID) - 100 FROM TeamBattles
            )
        ) AS X, Courses AS C
        WHERE X.CourseID = C.ID
        GROUP BY TBID
        ORDER BY Date DESC
    """)

    battles = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("team-battle-list", battles = battles)
