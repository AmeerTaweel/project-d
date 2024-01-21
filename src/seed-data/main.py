import argparse
from collections import Counter
from datetime import date, timedelta
import numpy as np
import pandas as pd


################################################################################
# Parse Arguments
################################################################################

POPULATE       = "populate"
COURSE_PROMPTS = "course-prompts"
COURSE_IMAGES  = "course-images"
TEAM_PROMPTS   = "team-prompts"
TEAM_IMAGES    = "team-images"
DRIVER_PROMPTS = "driver-prompts"
DRIVER_IMAGES  = "driver-images"
CAR_PROMPTS    = "car-prompts"
CAR_IMAGES     = "car-images"

parser = argparse.ArgumentParser(prog = "seed-data")

parser.add_argument("functionality", choices = [
    POPULATE,
    COURSE_PROMPTS,
    COURSE_IMAGES,
    TEAM_PROMPTS,
    TEAM_IMAGES,
    DRIVER_PROMPTS,
    DRIVER_IMAGES,
    CAR_PROMPTS,
    CAR_IMAGES
])

args = parser.parse_args()

func = args.functionality


################################################################################
# Load Courses
################################################################################


# Load InitialD Courses
courses_initial_d = pd.read_csv("./courses-initial-d.csv")

# Load Synthetic Courses
# Generated using ChatGPT 4
courses_synthetic = pd.read_csv("./courses-synthetic.csv")

# Combine Data
courses = pd.concat([courses_initial_d, courses_synthetic], ignore_index = True)


################################################################################
# Load Teams
################################################################################


# Load InitialD Teams
teams_initial_d = pd.read_csv("./teams-initial-d.csv")

# Load Synthetic Teams
# Generated using ChatGPT 4
teams_synthetic = pd.read_csv("./teams-synthetic.csv")

# Combine Data
teams = pd.concat([teams_initial_d, teams_synthetic], ignore_index = True)


################################################################################
# Load Drivers
################################################################################


# Load InitialD Drivers
drivers_initial_d = pd.read_csv("./drivers-initial-d.csv")

# Load Synthetic Drivers
# Generated using ChatGPT 4
drivers_synthetic = pd.read_csv("./drivers-synthetic.csv")

# Combine Data
drivers = pd.concat([drivers_initial_d, drivers_synthetic], ignore_index = True)


################################################################################
# Helpers
################################################################################


def gen_course_images():
    # Generate Image File Names
    images = []
    for i, row in courses.iterrows():
        name, location = row

        file_name = f"{name.lower().replace(' ', '-')}.png"

        images.append(f"images/courses/{file_name}")
    return images


def gen_team_images():
    # Generate Image File Names
    images = []
    for i, row in teams.iterrows():
        name, location = row

        file_name = f"{name.lower().replace(' ', '-')}.png"

        images.append(f"images/teams/{file_name}")
    return images


def gen_driver_images():
    # Generate Image File Names
    images = []
    for i, row in drivers.iterrows():
        name, team, car, gender = row

        file_name = f"{name.lower().replace(' ', '-')}.png"

        images.append(f"images/drivers/{file_name}")
    return images


def gen_car_images():
    # Generate Image File Names
    images = []
    for i, row in drivers.iterrows():
        name, team, car, gender = row

        file_name = f"{car.lower().replace(' ', '-')}.png"

        images.append(f"images/cars/{file_name}")
    return images


################################################################################
# Secondary Functionalities
################################################################################


def course_prompts():
    # Generate ChatGPT Prompts
    for i, row in courses.iterrows():
        name, location = row
        print(
            f"{name} is a street racing course in the {location}.",
            "Generate a picture for the racing course."
        )


def course_images():
    for image in gen_course_images():
        print(image.split("/")[-1])


def team_prompts():
    # Generate ChatGPT Prompts
    for i, row in teams.iterrows():
        name, location = row
        print(
            f"{name} is a Japanese street racing team based in {location}.",
            "Generate a logo for this team."
        )


def team_images():
    for image in gen_team_images():
        print(image.split("/")[-1])


def driver_prompts():
    # Generate ChatGPT Prompts
    for i, row in drivers.iterrows():
        name, team, car, gender = row
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


def driver_images():
    for image in gen_driver_images():
        print(image.split("/")[-1])


def car_prompts():
    # Generate ChatGPT Prompts
    for i, row in drivers.iterrows():
        name, team, car, gender = row
        print(f"Generate an image of {car} used for street racing.")


def car_images():
    for image in gen_car_images():
        print(image.split("/")[-1])


################################################################################
# Switch
################################################################################


if   func == COURSE_PROMPTS:
    course_prompts()
    exit()
elif func == COURSE_IMAGES:
    course_images()
    exit()
elif func == TEAM_PROMPTS:
    team_prompts()
    exit()
elif func == TEAM_IMAGES:
    team_images()
    exit()
elif func == DRIVER_PROMPTS:
    driver_prompts()
    exit()
elif func == DRIVER_IMAGES:
    driver_images()
    exit()
elif func == CAR_PROMPTS:
    car_prompts()
    exit()
elif func == CAR_IMAGES:
    car_images()
    exit()


################################################################################
# Main Functionality (Populate)
################################################################################


########################################
## Assign Teams To Synthetic Drivers
########################################


def assign_teams_synthetic():
    TEAM_TO_SOLO_RATIO = 0.5

    n = len(drivers_synthetic)

    team_count = int(TEAM_TO_SOLO_RATIO * n)
    solo_count = n - team_count

    rand_teams = np.random.choice(teams_synthetic.Name, size = team_count)
    none_teams = [None] * solo_count

    assignment = np.random.choice(
        np.array([*rand_teams, *none_teams]),
        size = n, replace = False
    )

    return drivers_synthetic.join(pd.DataFrame({"Team": assignment}))


drivers_initial_d = drivers_initial_d.replace({np.nan: None})
drivers_synthetic = assign_teams_synthetic()

drivers = pd.concat([drivers_initial_d, drivers_synthetic], ignore_index = True)

team_counts = Counter(list(drivers.Team))

print(f"Assigned {len(team_counts) - 1} teams out of {len(teams)}.")
print()
print("Team Counts:")
print(pd.DataFrame({
    "Team" : [k              for k in team_counts.keys() if k != None],
    "Count": [team_counts[k] for k in team_counts.keys() if k != None]
}).to_string(index = False))


########################################
## Assign Talent, Diligence, and Skills
## To Drivers
########################################


def assign_drivers_skills():
    TALENT_MEAN    = 0.5
    TALENT_STD     = 0.2
    DILIGENCE_MEAN = 0.5
    DILIGENCE_STD  = 0.2

    n = len(drivers)

    talent = np.random.normal(TALENT_MEAN, TALENT_STD, size = n)
    talent = [max(0, t) for t in talent]
    talent = [min(1, t) for t in talent]

    diligence = np.random.normal(DILIGENCE_MEAN, DILIGENCE_STD, size = n)
    diligence = [max(0, d) for d in diligence]
    diligence = [min(1, d) for d in diligence]
    
    return drivers.join(pd.DataFrame({
        "Talent"   : talent,
        "Diligence": diligence,
        "Skill"    : talent
    }))


drivers = assign_drivers_skills()


########################################
## Assign Length and Difficulty To
## Courses
########################################


def assign_course_length_and_difficulty():
    LEN_MEAN = 17
    LEN_STD  = 5
    DIF_MIN  = 0
    DIF_MAX  = 1

    n = len(courses)

    lens = np.random.normal(LEN_MEAN, LEN_STD, size = n)
    lens = [max(3, l) for l in lens]

    min_len = min(lens)
    max_len = max(lens)

    # Short tracks tend to be more difficult
    difs = [
        np.random.uniform(DIF_MIN + (1 - ((l - min_len) / (max_len - min_len))) * ((DIF_MAX - DIF_MIN) / 2), DIF_MAX)
        for l in lens
    ]

    return courses.join(pd.DataFrame({"Length": lens, "Difficulty": difs}))


courses = assign_course_length_and_difficulty()


########################################
## Generate Races And Time Attacks
########################################


DATE_BEGIN = date.fromisoformat("2019-01-01")
DATE_END   = date.fromisoformat("2024-01-23")


def sim_time(driver, course):
    SPEED_CONSTANT = 180
    MEAN_DIFF      = 15
    STD_DIFF       = 15

    skill      = drivers.Skill[driver]
    length     = courses.Length[course]
    difficulty = courses.Difficulty[course]

    speed_mean = SPEED_CONSTANT / (1 + difficulty)

    speed = np.random.normal(
        speed_mean + (skill * 2 - 1) * MEAN_DIFF,
        difficulty * (1 - skill) * STD_DIFF
    )

    time = length / speed

    return time


DELTA                  = timedelta(days = 1)
TIME_ATTACK_COUNT_MEAN = 3
TIME_ATTACK_COUNT_STD  = 1
P_INDIV                = 5 / 7
P_TEAM                 = 2 / 7

day = DATE_BEGIN

time_attacks       = []
individual_battles = []
team_battles       = []

while day <= DATE_END:
    day += DELTA

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

        time = sim_time(driver, course)

        time_attacks.append((driver, course, date, time))

    ####################
    ### Indiv. Battles
    ####################

    indiv_battle_happened = np.random.choice([True, False], p = [P_INDIV, 1 - P_INDIV])

    if indiv_battle_happened:
        # Pick Drivers
        driver1, driver2 = np.random.choice(len(drivers), 2, replace = False)
        # Pick Course
        course = np.random.choice(len(courses))

        time1 = sim_time(driver1, course)
        time2 = sim_time(driver2, course)

        if time1 == time2:
            print("Draw in individual battles.")

        individual_battles.append((driver1, driver2, course, date, time1, time2))

    ####################
    ### Team Battles
    ####################

    team_battle_happened = np.random.choice([True, False], p = [P_TEAM, 1 - P_TEAM])

    if team_battle_happened:
        # Pick Teams
        team1, team2 = np.random.choice(len(teams), 2, replace = False)
        # Get Individual Battles Count
        team1_name = teams.Name[team1]
        team1_drivers = drivers[drivers.Team == team1_name]
        team2_name = teams.Name[team2]
        team2_drivers = drivers[drivers.Team == team2_name]
        battle_count = min(len(team1_drivers), len(team2_drivers))
        # Pick Top Drivers From Each Team
        team1_participants = team1_drivers.sort_values(by = "Skill", ascending = False)
        team1_participants = list(team1_participants.iloc[:battle_count].index)
        team2_participants = team2_drivers.sort_values(by = "Skill", ascending = False)
        team2_participants = list(team2_participants.iloc[:battle_count].index)

        # Pick Course
        course = np.random.choice(len(courses))

        battle = []

        points1 = 0
        points2 = 0

        for driver1, driver2 in zip(team1_participants, team2_participants):
            time1 = sim_time(driver1, course)
            time2 = sim_time(driver2, course)
            if time1 < time2: points1 += 1
            if time2 < time1: points2 += 1
            battle.append((driver1, driver2, time1, time2))

        # No Draws
        i = 0
        while points1 == points2:
            driver1 = team1_participants[i]
            driver2 = team2_participants[i]
            time1 = sim_time(driver1, course)
            time2 = sim_time(driver2, course)
            if time1 < time2: points1 += 1
            if time2 < time1: points2 += 1
            battle.append((driver1, driver2, time1, time2))
            i += 1
            i = i % battle_count

        team_battles.append((team1, team2, course, date, battle))

    ####################
    ### Racers Progress
    ####################

    SKILL_DIFF = 1 / (DATE_END - DATE_BEGIN).days
    for i in range(len(drivers)):
        diligence = drivers.Diligence[i]
        diligence = diligence * 2 - 1
        skill     = drivers.Skill[i]
        progress  = min(1, max(-1, np.random.normal(diligence)))
        skill     = skill + progress * SKILL_DIFF
        skill     = min(1, max(0, skill))
        drivers.loc[i, "Skill"] = skill

print(f"Simulated {len(time_attacks)} time attacks.")
print(f"Simulated {len(individual_battles)} individual battles.")
print(f"Simulated {len(team_battles)} team battles.")
