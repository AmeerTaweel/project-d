from bottle import template

def driver_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    db_cursor.execute(f"""
        WITH X AS (
            SELECT R1.BattleID AS BID, D1.ID AS D1ID, D1.Name AS D1Name, D2.ID
                   AS D2ID, D2.Name AS D2Name, R1.Minutes AS R1Min,
                   R2.Minutes AS R2Min, R1.Date AS Date
            FROM Drivers AS D1, Drivers AS D2, Records AS R1, Records AS R2
            WHERE R1.ID <> R2.ID
            AND D1.ID = R1.DriverID
            AND D2.ID = R2.DriverID
            AND R1.BattleID = R2.BattleID
            AND R1.BattleID IS NOT NULL
            AND (R1.Minutes < R2.Minutes OR (R1.Minutes = R2.Minutes AND D1.ID < D2.ID))
        )
        SELECT Drivers.*, Teams.Name, W.Count, D.Count, L.Count
        FROM Drivers
        LEFT OUTER JOIN Teams
        ON Drivers.TeamID = Teams.ID
        LEFT OUTER JOIN (
            SELECT D1ID AS DID, D1Name AS DName, COUNT(*) AS Count
            FROM X
            WHERE R1Min < R2Min
            GROUP BY D1ID
        ) AS W
        ON Drivers.ID = W.DID
        LEFT OUTER JOIN (
            SELECT DID, DName, COUNT(*) AS Count
            FROM ((
                SELECT D1ID AS DID, D1Name AS DName, BID
                FROM X
                WHERE R1Min = R2Min
            ) UNION (
                SELECT D2ID AS DID, D2Name AS DName, BID
                FROM X
                WHERE R1Min = R2Min
            )) AS Y
            GROUP BY DID
        ) AS D
        ON Drivers.ID = D.DID
        LEFT OUTER JOIN (
            SELECT D2ID AS DID, D2Name AS DName, COUNT(*) AS Count
            FROM X
            WHERE R1Min < R2Min
            GROUP BY D2ID
        ) AS L
        ON Drivers.ID = L.DID
    """)

    drivers = [row for row in db_cursor]

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("driver-list", drivers = drivers)
