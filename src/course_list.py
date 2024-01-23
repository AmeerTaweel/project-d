from bottle import template

def course_list(db_name, db_connection):
    # Get Databse Cursor
    db_cursor = db_connection.cursor(buffered = True)
    db_cursor.execute(f"USE {db_name}")

    # Execute Query
    db_cursor.execute("SELECT * FROM Courses")

    # Get Results
    courses = tuple(row for row in db_cursor)

    # Close Database Cursor
    db_cursor.close()

    # Pass to Template
    return template("course-list", courses = courses)
