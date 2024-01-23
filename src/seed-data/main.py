import argparse
import re
from collections import Counter
from datetime import date, timedelta
import numpy as np
import mysql.connector


################################################################################
# Constants
################################################################################


# Commands / Functionalities
POPULATE       = "populate"
COURSE_PROMPTS = "course-prompts"
COURSE_IMAGES  = "course-images"
TEAM_PROMPTS   = "team-prompts"
TEAM_IMAGES    = "team-images"
DRIVER_PROMPTS = "driver-prompts"
DRIVER_IMAGES  = "driver-images"

TEAM_TO_SOLO_RATIO = 0.5

DB_NAME     = "projectd"
DB_HOST     = "localhost"
DB_USERNAME = "root"

SKILL_MEAN    = 0.5
SKILL_STD     = 0.2

LEN_MEAN = 17
LEN_STD  = 5
LEN_MIN  = 3
DIF_MIN  = 0
DIF_MAX  = 1

DATE_BEGIN = date.fromisoformat("2019-01-01")
DATE_END   = date.fromisoformat("2024-01-23")

SPEED_CONSTANT = 180
MEAN_DIFF      = 15
STD_DIFF       = 15

DELTA                  = timedelta(days = 1)
TIME_ATTACK_COUNT_MEAN = 3
TIME_ATTACK_COUNT_STD  = 1
P_INDIV                = 5 / 7
P_TEAM                 = 2 / 7


################################################################################
# Parse Arguments
################################################################################

parser = argparse.ArgumentParser(prog = "seed-data")

parser.add_argument("functionality", choices = [
    POPULATE,
    COURSE_PROMPTS,
    COURSE_IMAGES,
    TEAM_PROMPTS,
    TEAM_IMAGES,
    DRIVER_PROMPTS,
    DRIVER_IMAGES
])

parser.add_argument("-s", "--seed",  type = int,  default = 0)
parser.add_argument("-f", "--force", action = "store_true")

args = parser.parse_args()

# Arguments
func  = args.functionality
seed  = args.seed
force = args.force


################################################################################
# Set Random Seed
################################################################################


np.random.seed(seed)


################################################################################
# Helper Functions
################################################################################


def load_csv(file_name):
    return np.genfromtxt(
        file_name,
        delimiter = ",",
        dtype = None,
        skip_header = 1,
        encoding = "utf8"
    )


def get_filename(name, ext):
    filename_dirty = name.lower().replace(" ", "-")
    filename_clean = re.sub(r"[^a-zA-Z0-9\-]", "", filename_dirty)
    return f"{filename_clean}.{ext}"


def gen_image_column(entity_type, name_column):
    return [
        f"images/{entity_type}/{get_filename(name, 'png')}"
        for name in name_column
    ]


################################################################################
# Load Data
################################################################################


# Load InitialD Courses
# Name, Location
courses_initial_d = load_csv("./courses-initial-d.csv")

# Load Synthetic Courses
# Generated using ChatGPT 4
# Name, Location
courses_synthetic = load_csv("./courses-synthetic.csv")

# Combine Courses
courses = np.r_[courses_initial_d, courses_synthetic]

# Load InitialD Teams
# Name, Location
teams_initial_d = load_csv("./teams-initial-d.csv")

# Load Synthetic Teams
# Generated using ChatGPT 4
# Name, Location
teams_synthetic = load_csv("./teams-synthetic.csv")

# Combine Teams
teams = np.r_[teams_initial_d, teams_synthetic]

# Load InitialD Drivers
# Name, Team, Car, Gender
drivers_initial_d = load_csv("./drivers-initial-d.csv")

# Load Synthetic Drivers
# Generated using ChatGPT 4
# Name, Car, Gender
drivers_synthetic = load_csv("./drivers-synthetic.csv")


def gen_synthetic_driver_teams(drivers_synthetic, teams_synthetic):
    n = len(drivers_synthetic)

    team_count = int(TEAM_TO_SOLO_RATIO * n)
    solo_count = n - team_count

    rand_teams = np.random.choice(teams_synthetic[:, 0], size = team_count)
    none_teams = np.repeat("", solo_count)

    teams = np.random.choice(
        np.r_[rand_teams, none_teams],
        size = n, replace = False
    )

    names   = drivers_synthetic[:, 0]
    cars    = drivers_synthetic[:, 1]
    genders = drivers_synthetic[:, 2]

    return np.c_[names, teams, cars, genders]


# Assign synthetic drivers to synthetic teams
drivers_synthetic = gen_synthetic_driver_teams(drivers_synthetic, teams_synthetic)

if func == POPULATE:
    team_counts = Counter(drivers_synthetic[:, 1])
    max_team_name_len = max([len(k) for k in team_counts])
    print(f"Assigned {len(team_counts) - 1} teams out of {len(teams_synthetic)}.")
    print()
    print("Team Counts:")
    for team, count in team_counts.items():
        if team == "": continue
        print(f"{team.ljust(max_team_name_len)} -> {count}")

# Combine Drivers
drivers = np.r_[drivers_initial_d, drivers_synthetic]


def get_team_indices(drivers, teams):
    team_indices = np.arange(len(teams))
    team_names   = teams[:, 0]
    driver_teams = drivers[:, 1]

    driver_team_indices = np.array([
        team_indices[team_names == t][0] if t in team_names else None
        for t in driver_teams
    ])

    driver_names   = drivers[:, 0]
    driver_cars    = drivers[:, 2]
    driver_genders = drivers[:, 3]

    return np.c_[driver_names, driver_team_indices, driver_cars, driver_genders]


# Replace team name by team index
drivers = get_team_indices(drivers, teams)


################################################################################
# Add Image Names
################################################################################


courses = np.c_[courses, gen_image_column("courses", courses[:, 0])]
teams   = np.c_[teams, gen_image_column("teams", teams[:, 0])]
drivers = np.c_[drivers, gen_image_column("drivers", drivers[:, 0])]


################################################################################
# Secondary Functionalities
################################################################################


def course_prompts(courses):
    # Generate ChatGPT Prompts
    for name, loc, _ in courses:
        print(
            f"{name} is a street racing course in the {loc}.",
            "Generate a picture for the racing course."
        )


def course_images(courses):
    for _, _, image in courses:
        print(image.split("/")[-1])


def team_prompts(teams):
    # Generate ChatGPT Prompts
    for name, loc, _ in teams:
        print(
            f"{name} is a Japanese street racing team based in {loc}.",
            "Generate a logo for this team."
        )


def team_images(teams):
    for _, _, image in teams:
        print(image.split("/")[-1])


def driver_prompts(drivers):
    # Generate ChatGPT Prompts
    for name, _, car, gender, _ in drivers:
        if gender == "Male":
            print(
                f"{name} is a street driver.",
                "He is a male.",
                f"He drives a {car}.",
                f"Generate a profile picture of him."
            )
        else:
            print(
                f"{name} is a street driver.",
                "She is a female.",
                f"She drives drives a {car}.",
                f"Generate a profile picture of her."
            )


def driver_images(drivers):
    for _, _, _, _, image  in drivers:
        print(image.split("/")[-1])


if   func == COURSE_PROMPTS:
    course_prompts(courses)
    exit()
elif func == COURSE_IMAGES:
    course_images(courses)
    exit()
elif func == TEAM_PROMPTS:
    team_prompts(teams)
    exit()
elif func == TEAM_IMAGES:
    team_images(teams)
    exit()
elif func == DRIVER_PROMPTS:
    driver_prompts(drivers)
    exit()
elif func == DRIVER_IMAGES:
    driver_images(drivers)
    exit()


################################################################################
# Main Functionality (Populate)
################################################################################


########################################
## Initialize Database
########################################


# Connect to database
db_connection = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USERNAME
)

# Create database cursor to perform SQL operation and run queries
db_cursor = db_connection.cursor(buffered = True)

# Check if database exists
db_cursor.execute("SHOW DATABASES")
db_list = [row[0] for row in db_cursor]

if DB_NAME in db_list:
    if not force:
        print(f"ERROR: Database {DB_NAME} already exists.")
        exit()
    db_cursor.execute(f"DROP DATABASE {DB_NAME}")

db_cursor.execute(f"CREATE DATABASE {DB_NAME}")
print(f"Created database {DB_NAME}.")


########################################
## Assign Talent, Diligence, and Skills
## To Drivers
########################################


def assign_drivers_skills(drivers):
    n = len(drivers)

    skill = np.random.normal(SKILL_MEAN, SKILL_STD, size = n)
    skill = np.clip(skill, 0, 1)

    return np.c_[drivers, skill]


drivers = assign_drivers_skills(drivers)

skills = drivers[:, 5]
print()
just = lambda criteria : str(len(skills[criteria])).rjust(len(str(len(drivers))))
print(f"Drivers with skill == 0          : {just(skills == 0)}")
print(f"Drivers with skill in (0,   0.05]: {just(np.logical_and((skills > 0), (skills <= 0.05)))}")
print(f"Drivers with skill in (0.05, 0.1]: {just(np.logical_and((skills > 0.05), (skills <= 0.1)))}")
print(f"Drivers with skill in (0.1,  0.5]: {just(np.logical_and((skills > 0.1), (skills <= 0.5)))}")
print(f"Drivers with skill in (0.5,  0.9]: {just(np.logical_and((skills > 0.5), (skills <= 0.9)))}")
print(f"Drivers with skill in (0.9, 0.95]: {just(np.logical_and((skills > 0.9), (skills <= 0.95)))}")
print(f"Drivers with skill == 1          : {just(skills == 1)}")


########################################
## Assign Length and Difficulty To
## Courses
########################################


def assign_course_length_and_difficulty(courses):
    n = len(courses)

    lens = np.random.normal(LEN_MEAN, LEN_STD, size = n)
    lens = np.clip(lens, LEN_MIN, None)

    min_len = float(np.min(lens))
    max_len = float(np.max(lens))
    rng_len = max_len - min_len

    # Short tracks tend to be more difficult
    difs = [
        np.random.uniform(
            DIF_MIN + (1 - ((l - min_len) / rng_len)) * ((DIF_MAX - DIF_MIN) / 2),
            DIF_MAX
        )
        for l in lens
    ]

    return np.c_[courses, lens, difs]


courses = assign_course_length_and_difficulty(courses)


########################################
## Generate Races And Time Attacks
########################################


def sim_time(driver, course):
    skill      = float(driver[5])
    length     = float(course[3])
    difficulty = float(course[4])

    speed_mean = SPEED_CONSTANT / (1 + difficulty)

    # Small randomness to break ties
    rand = np.random.uniform(-0.01, 0.01)

    speed = np.random.normal(
        speed_mean + (skill * 2 - 1) * MEAN_DIFF + rand,
        difficulty * (1 - skill) * STD_DIFF
    )

    time = length / speed

    return time


day = DATE_BEGIN

time_attacks       = ()
individual_battles = ()
team_battles       = ()

print()

while day < DATE_END:
    print(f"\rSimulating Day {day}...", end = "")

    ####################
    ### Time Attacks
    ####################

    time_attack_count = np.random.normal(TIME_ATTACK_COUNT_MEAN, TIME_ATTACK_COUNT_STD)
    time_attack_count = int(max(0, round(time_attack_count)))

    for _ in range(time_attack_count):
        # Pick Driver
        driver = np.random.choice(len(drivers))
        # Pick Course
        course = np.random.choice(len(courses))

        time = sim_time(drivers[driver], courses[course])

        time_attacks = (*time_attacks, (driver, course, day, time))

    ####################
    ### Indiv. Battles
    ####################

    indiv_battle_happened = np.random.choice([True, False], p = [P_INDIV, 1 - P_INDIV])

    if indiv_battle_happened:
        # Pick Drivers
        driver1, driver2 = np.random.choice(len(drivers), 2, replace = False)
        # Pick Course
        course = np.random.choice(len(courses))

        time1 = sim_time(drivers[driver1], courses[course])
        time2 = sim_time(drivers[driver2], courses[course])

        if time1 == time2:
            print("\rDraw in individual battles.")

        individual_battles = (
            *individual_battles,
            (driver1, driver2, course, day, time1, time2)
        )

    ####################
    ### Team Battles
    ####################

    team_battle_happened = np.random.choice([True, False], p = [P_TEAM, 1 - P_TEAM])

    if team_battle_happened:
        # Pick Teams
        team1, team2 = np.random.choice(len(teams), 2, replace = False)
        # Get Individual Battles Count
        team1_drivers = np.arange(len(drivers))[drivers[:, 1] == team1]
        team2_drivers = np.arange(len(drivers))[drivers[:, 1] == team2]
        battle_count = min(len(team1_drivers), len(team2_drivers))
        # Pick Top Drivers From Each Team
        team1_drivers = team1_drivers[np.argsort(drivers[team1_drivers, 5])]
        team1_drivers = team1_drivers[:battle_count]
        team2_drivers = team2_drivers[np.argsort(drivers[team1_drivers, 5])]
        team2_drivers = team2_drivers[:battle_count]

        # Pick Course
        course = np.random.choice(len(courses))

        battles = ()

        points1 = 0
        points2 = 0

        for driver1, driver2 in zip(team1_drivers, team2_drivers):
            time1 = sim_time(drivers[driver1], courses[course])
            time2 = sim_time(drivers[driver2], courses[course])
            if time1 < time2: points1 += 1
            if time2 < time1: points2 += 1
            battles = (*battles, (driver1, driver2, time1, time2))

        # No Draws
        i = 0
        while points1 == points2:
            driver1 = team1_drivers[i]
            driver2 = team2_drivers[i]
            time1 = sim_time(drivers[driver1], courses[course])
            time2 = sim_time(drivers[driver2], courses[course])
            if time1 < time2: points1 += 1
            if time2 < time1: points2 += 1
            battles = (*battles, (driver1, driver2, time1, time2))
            i += 1
            i = i % battle_count

        team_battles = (*team_battles, (team1, team2, course, day, battles))

    day += DELTA


print("\r")
max_num_len = max([len(str(len(i))) for i in (time_attacks, individual_battles, team_battles)])
print(f"Simulated {str(len(time_attacks)).rjust(max_num_len)} time       attacks.")
print(f"Simulated {str(len(individual_battles)).rjust(max_num_len)} individual battles.")
print(f"Simulated {str(len(team_battles)).rjust(max_num_len)} team       battles.")


########################################
## Create Tables
########################################


# Use database in the following queries
db_cursor.execute(f"USE {DB_NAME}")

# Courses Table
db_cursor.execute("""
    CREATE TABLE Courses (
        ID   INT          NOT NULL AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL,
        Loc  VARCHAR(255) NOT NULL,
        Len  DOUBLE       NOT NULL,
        Img  VARCHAR(255) NOT NULL,
        PRIMARY KEY (ID)
    )
""")

# Teams Table
db_cursor.execute("""
    CREATE TABLE Teams (
        ID   INT          NOT NULL AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL,
        Loc  VARCHAR(255) NOT NULL,
        Logo VARCHAR(255) NOT NULL,
        PRIMARY KEY (ID)
    )
""")

# Drivers Table
db_cursor.execute("""
    CREATE TABLE Drivers (
        ID     INT          NOT NULL AUTO_INCREMENT,
        Name   VARCHAR(255) NOT NULL,
        Car    VARCHAR(255) NOT NULL,
        TeamID INT,
        Sex    VARCHAR(255) NOT NULL,
        Pic    VARCHAR(255) NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (TeamID) REFERENCES Teams(ID)
    )
""")

# Team Battles Table
db_cursor.execute("""
    CREATE TABLE TeamBattles (
        ID INT NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (ID)
    )
""")

# Battles Table
db_cursor.execute("""
    CREATE TABLE Battles (
        ID           INT NOT NULL AUTO_INCREMENT,
        TeamBattleID INT,
        PRIMARY KEY (ID),
        FOREIGN KEY (TeamBattleID) REFERENCES TeamBattles(ID)
    )
""")

# Records Table
db_cursor.execute("""
    CREATE TABLE Records (
        ID       INT    NOT NULL AUTO_INCREMENT,
        DriverID INT    NOT NULL,
        CourseID INT    NOT NULL,
        Date     DATE   NOT NULL,
        Minutes  DOUBLE NOT NULL,
        BattleID INT,
        PRIMARY KEY (ID),
        FOREIGN KEY (DriverID) REFERENCES Drivers(ID),
        FOREIGN KEY (CourseID) REFERENCES Courses(ID),
        FOREIGN KEY (BattleID) REFERENCES Battles(ID)
    )
""")


########################################
## Insert Data
########################################


# Courses

for name, loc, image, len, _ in courses:
    db_cursor.execute(f"""
        INSERT INTO Courses (Name, Loc, Len, Img) VALUES (
            "{name}", "{loc}", {len}, "{image}"
        )
    """)

# Teams

for name, loc, logo in teams:
    db_cursor.execute(f"""
        INSERT INTO Teams (Name, Loc, Logo) VALUES (
            "{name}", "{loc}", "{logo}"
        )
    """)

# Drivers

for name, team, car, gender, pic, _ in drivers:
    team = int(team) + 1 if team != None else "NULL"
    db_cursor.execute(f"""
        INSERT INTO Drivers (Name, Car, TeamID, Sex, Pic) VALUES (
            "{name}", "{car}", {team}, "{gender}", "{pic}"
        )
    """)

# Time Attacks

for driver, course, day, time in time_attacks:
    db_cursor.execute(f"""
        INSERT INTO Records (DriverID, CourseID, Date, Minutes, BattleID) VALUES (
            {driver + 1}, {course + 1}, "{day}", {time * 60}, NULL
        )
    """)

# Individual Battles

battle_id = 0

for driver1, driver2, course, day, time1, time2 in individual_battles:
    db_cursor.execute(f"""
        INSERT INTO Battles (TeamBattleID) VALUES (NULL)
    """)
    battle_id += 1
    db_cursor.execute(f"""
        INSERT INTO Records (DriverID, CourseID, Date, Minutes, BattleID) VALUES (
            {driver1 + 1}, {course + 1}, "{day}", {time1 * 60}, {battle_id}
        ), (
            {driver2 + 1}, {course + 1}, "{day}", {time2 * 60}, {battle_id}
        )
    """)

# Insert Team Battles

team_battle_id = 0

for team1, team2, course, day, battle in team_battles:
    db_cursor.execute(f"""
        INSERT INTO TeamBattles () VALUES ()
    """)
    team_battle_id += 1
    for driver1, driver2, time1, time2 in battle:
        db_cursor.execute(f"""
            INSERT INTO Battles (TeamBattleID) VALUES ({team_battle_id})
        """)
        battle_id += 1
        db_cursor.execute(f"""
            INSERT INTO Records (DriverID, CourseID, Date, Minutes, BattleID) VALUES (
                {driver1 + 1}, {course + 1}, "{day}", {time1 * 60}, {battle_id}
            ), (
                {driver2 + 1}, {course + 1}, "{day}", {time2 * 60}, {battle_id}
            )
        """)

db_connection.commit()
db_connection.close()
