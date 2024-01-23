from bottle import template, abort

def team_info(db_name, db_connection, id):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        SELECT *
        FROM Teams
        WHERE ID = {id}
    """)

    teams = tuple(row for row in db_cursor)

    if len(teams) != 1:
        # Close Database Cursor
        db_cursor.close()
        abort(404)
        return

    team = teams[0]

    # Get Team Members
    db_cursor.execute(f"""
        SELECT *
        FROM Drivers
        WHERE TeamID = {id}
    """)

    members = tuple(row for row in db_cursor)

    db_cursor.execute(f"""
        SELECT COUNT(IF(Y.Points1 > Y.Points2, 1, NULL)) AS Wins,
               COUNT(IF(Y.Points1 < Y.Points2, 1, NULL)) AS Losses
        FROM (
            SELECT COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
                   COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
            FROM (
                SELECT B.TeamBattleID AS TeamBAttleID,
                       B.ID AS BattleID,
                       R1.Minutes AS Min1,
                       R2.Minutes AS Min2
                FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                     Battles AS B
                WHERE R1.ID <> R2.ID
                AND D1.ID = R1.DriverID
                AND D2.ID = R2.DriverID
                AND R1.BattleID = R2.BattleID
                AND R1.BattleID IS NOT NULL
                AND R2.BattleID = B.ID
                AND B.TeamBattleID IS NOT NULL
                AND R1.Minutes <> R2.Minutes
                AND D1.TeamID = {id}
            ) AS X
            GROUP BY X.TeamBAttleID
        ) AS Y
    """)

    wl = tuple(row for row in db_cursor)[0]

    db_cursor.execute(f"""
        SELECT X.TeamBattleID, T.ID, T.Name, X.Date,
               COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
               COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
        FROM (
            SELECT B.TeamBattleID AS TeamBAttleID,
                   B.ID AS BattleID,
                   R1.Minutes AS Min1,
                   R2.Minutes AS Min2,
                   D2.TeamID AS TID,
                   R1.Date
            FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                 Battles AS B
            WHERE R1.ID <> R2.ID
            AND D1.ID = R1.DriverID
            AND D2.ID = R2.DriverID
            AND R1.BattleID = R2.BattleID
            AND R1.BattleID IS NOT NULL
            AND R2.BattleID = B.ID
            AND B.TeamBattleID IS NOT NULL
            AND R1.Minutes <> R2.Minutes
            AND D1.TeamID = {id}
        ) AS X, Teams AS T
        WHERE X.TID = T.ID
        GROUP BY X.TeamBAttleID
        ORDER BY Date DESC
    """)

    all_team_battles = tuple(row for row in db_cursor)

    db_cursor.execute(f"""
        SELECT C.ID, C.Name,
               COUNT(IF(Y.Points1 > Y.Points2, 1, NULL)) AS Wins,
               COUNT(IF(Y.Points1 < Y.Points2, 1, NULL)) AS Losses
        FROM (
            SELECT X.CID AS CID,
                   COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
                   COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
            FROM (
                SELECT B.TeamBattleID AS TeamBAttleID,
                       B.ID AS BattleID,
                       R1.Minutes AS Min1,
                       R2.Minutes AS Min2,
                       R1.CourseID As CID
                FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                     Battles AS B
                WHERE R1.ID <> R2.ID
                AND D1.ID = R1.DriverID
                AND D2.ID = R2.DriverID
                AND R1.BattleID = R2.BattleID
                AND R1.BattleID IS NOT NULL
                AND R2.BattleID = B.ID
                AND B.TeamBattleID IS NOT NULL
                AND R1.Minutes <> R2.Minutes
                AND D1.TeamID = {id}
            ) AS X
            GROUP BY X.TeamBAttleID
        ) AS Y, Courses AS C
        WHERE Y.CID = C.ID
        GROUP BY Y.CID
        ORDER BY C.ID ASC
    """)

    wl_per_course = tuple(row for row in db_cursor)

    db_cursor.execute(f"""
        SELECT T.ID, T.Name,
               COUNT(IF(Y.Points1 > Y.Points2, 1, NULL)) AS Wins,
               COUNT(IF(Y.Points1 < Y.Points2, 1, NULL)) AS Losses
        FROM (
            SELECT X.TID AS TID,
                   COUNT(IF(X.Min1 < X.Min2, 1, NULL)) AS Points1,
                   COUNT(IF(X.Min1 > X.Min2, 1, NULL)) AS Points2
            FROM (
                SELECT B.TeamBattleID AS TeamBAttleID,
                       B.ID AS BattleID,
                       R1.Minutes AS Min1,
                       R2.Minutes AS Min2,
                       D2.TeamID AS TID
                FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2,
                     Battles AS B
                WHERE R1.ID <> R2.ID
                AND D1.ID = R1.DriverID
                AND D2.ID = R2.DriverID
                AND R1.BattleID = R2.BattleID
                AND R1.BattleID IS NOT NULL
                AND R2.BattleID = B.ID
                AND B.TeamBattleID IS NOT NULL
                AND R1.Minutes <> R2.Minutes
                AND D1.TeamID = {id}
            ) AS X
            GROUP BY X.TeamBAttleID
        ) AS Y, Teams AS T
        WHERE Y.TID = T.ID
        GROUP BY Y.TID
        ORDER BY T.ID ASC
    """)

    wl_per_team = tuple(row for row in db_cursor)

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template(
        "team-info",
        team = team,
        members = members,
        wl = wl,
        all_team_battles = all_team_battles,
        wl_per_course = wl_per_course,
        wl_per_team = wl_per_team
    )
