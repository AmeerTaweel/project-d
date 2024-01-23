from bottle import route, run, template, static_file
import mysql.connector

from course_list import course_list
from course_info import course_info
from driver_list import driver_list
from driver_info import driver_info
from team_list   import team_list
from team_info   import team_info
from record_list import record_list
from record_info import record_info
from battle_list import battle_list
from battle_info import battle_info
from team_battle_list import team_battle_list
from team_battle_info import team_battle_info


DB_NAME     = "projectd"
DB_HOST     = "localhost"
DB_USERNAME = "root"

SERVER_HOST = "localhost"
SERVER_PORT = 8080


# Connect to database
db_connection = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USERNAME
)


# Serve Static Directory
@route("/static/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root = "./seed-data")


# Serve Favicon
@route("/favicon.ico")
def serve_favicon():
    return static_file("images/favicon.ico", root = "./seed-data")


# Main (Index) Page
@route("/")
def index_route():
    return template("index")


# Course List Page
@route("/courses")
def course_list_route():
    return course_list(DB_NAME, db_connection)


# Course Info Page
@route("/courses/<id>")
def course_info_route(id):
    return course_info(DB_NAME, db_connection, id)


# Driver List Page
@route("/drivers")
def driver_list_route():
    return driver_list(DB_NAME, db_connection)


# Driver Info Page
@route("/drivers/<id>")
def driver_info_route(id):
    return driver_info(DB_NAME, db_connection, id)


# Team List Page
@route("/teams")
def team_list_route():
    return team_list(DB_NAME, db_connection)


# Team Info Page
@route("/teams/<id>")
def team_info_route(id):
    return team_info(DB_NAME, db_connection, id)


# Record List Page
@route("/records")
def record_list_route():
    return record_list(DB_NAME, db_connection)


# Record Info Page
@route("/records/<id>")
def record_info_route(id):
    return record_info(DB_NAME, db_connection, id)


# Battle List Page
@route("/battles")
def battle_list_route():
    return battle_list(DB_NAME, db_connection)


# Battle Info Page
@route("/battles/<id>")
def battle_info_route(id):
    return battle_info(DB_NAME, db_connection, id)


# Team Battle List Page
@route("/team-battles")
def team_battle_list_route():
    return team_battle_list(DB_NAME, db_connection)


# Team Battle Info Page
@route("/team-battles/<id>")
def team_battle_info_route(id):
    return team_battle_info(DB_NAME, db_connection, id)


run(host = SERVER_HOST, port = SERVER_PORT)

# Close Database Connection
db_connection.close()
