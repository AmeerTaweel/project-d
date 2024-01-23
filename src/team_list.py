from bottle import template

def team_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT Z.*, COUNT(*)
        FROM (
            SELECT Y.TID AS TID, Y.TName AS TName, Y.TLoc AS TLoc, Y.TLogo AS TLogo,
            COUNT(IF(Y.Points1 > Y.Points2, 1, NULL)) AS Wins,
            COUNT(IF(Y.Points1 < Y.Points2, 1, NULL)) AS Losses
            FROM (
                SELECT X.TID AS TID, X.TName AS TName, X.TLoc AS TLoc, X.TLogo AS TLogo,
                COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
                COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
                FROM (
                    SELECT B.TeamBattleID AS TeamBAttleID,
                           B.ID AS BattleID,
                           R1.Minutes AS Min1,
                           R2.Minutes AS Min2,
                           R1.CourseID AS CourseID,
                           R1.Date AS Date,
                           T.ID AS TID,
                           T.Name AS TName,
                           T.Loc AS TLoc,
                           T.Logo AS TLogo
                    FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                         Battles AS B, Teams AS T
                    WHERE R1.ID <> R2.ID
                    AND D1.ID = R1.DriverID
                    AND D2.ID = R2.DriverID
                    AND R1.BattleID = R2.BattleID
                    AND R1.BattleID IS NOT NULL
                    AND R2.BattleID = B.ID
                    AND B.TeamBattleID IS NOT NULL
                    AND R1.Minutes <> R2.Minutes
                    AND D1.TeamID = T.ID
                ) AS X
                GROUP BY X.TeamBAttleID, X.TID
            ) AS Y
            GROUP BY Y.TID
        ) AS Z, Drivers
        WHERE Drivers.TeamID = Z.TID
        GROUP BY Z.TID
    """)

    teams = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("team-list", teams = teams)
