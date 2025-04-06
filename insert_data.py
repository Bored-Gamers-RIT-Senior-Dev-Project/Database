#!/usr/bin/env python3
import getpass
import math
import random
import string
import sys
from datetime import datetime, timedelta

import mysql.connector
from faker import Faker

fake = Faker()

MYSQL_USER = "root"
MYSQL_HOST = "localhost"
MYSQL_DB = "BoardGame"

MYSQL_PASSWORD = getpass.getpass("Enter your database password: ")

try:
    conn = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB
    )
    cursor = conn.cursor()
    print("Connected to the database successfully!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()


def insert_universities(n=20):
    # List of valid university image URLs
    image_urls = [
        "https://imgs.search.brave.com/R3hK9P_n5HgZ1cGuiyXqq1VXFYLNyhKb1MvEZdxT2uU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTg0/NTkxMzUwL3Bob3Rv/L29oaW8tc3RhdGUt/dW5pdmVyc2l0eS5q/cGc_cz02MTJ4NjEy/Jnc9MCZrPTIwJmM9/OUtlaW9rX0V5RERJ/aUtSeGs4cG5lb0ls/UzJLQUVpdVBhcjZH/bVZqVWlxOD0",
        "https://imgs.search.brave.com/5sFTqF4iwvQs0p8PAMeFnH0LlIPPs5wRgK55Vs2Cvlo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTQ1/NTUyMzgyOS9waG90/by91Y2xhLWNvcnJp/ZG9yLmpwZz9zPTYx/Mng2MTImdz0wJms9/MjAmYz1YUHFrQjdx/cU9obGFvUU1TYkt2/WDBkdDdNdy1mTUx1/LWZYcmlPNUpBbVZJ/PQ",
        "https://imgs.search.brave.com/NbdsyUY0jjUWBtyRwzVc0gHwAhNYQRJ7moDHXnu6fJY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTU3/MzMyMzE4L3Bob3Rv/L3VuaXZlcnNpdHkt/Y2FtcHVzLWhhcnZh/cmQuanBnP3M9NjEy/eDYxMiZ3PTAmaz0y/MCZjPW05TlBiSGVZ/OFV4bHdUbDNwQVA3/eDNDSkthVWhGNkdl/ZlRGNm5PSzZkOFk9",
        "https://imgs.search.brave.com/7mT1c3UY7ud44Xz9FX-f8w1cGZFPlrJoAx-qyvbDpmI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTQ2/OTkzNzU2MS9waG90/by9saWJyYXJ5LWlu/dGVyaW9yLW94Zm9y/ZC11bml2ZXJzaXR5/LW94Zm9yZC1lbmds/YW5kLmpwZz9zPTYx/Mng2MTImdz0wJms9/MjAmYz1YZlJlQjhl/czNyWElVT0R0Tnc4/YW5CclZmSjVUWG9w/WEhNQkFGT2pPWEo4/PQ",
        "https://imgs.search.brave.com/uMJmh-IT71Ca4mTiU4FmqC6Aa2UXgZn1INMxPV__L1A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTU3/NTA1Mzk3L3Bob3Rv/L3F1YW5kcmFuZ2xl/LWxhd24tYXQtdGhl/LXVuaXZlcnNpdHkt/b2Ytd2FzaGluZ3Rv/bi5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9eTFUSWZmZ1Fh/TE44QW94WkNFeE54/bF93S29lTXE5eEl5/M19rYjhYWTJZZz0",
        "https://imgs.search.brave.com/7HqbXdPpjK5W71GqtuOsijkxtGmeWKL-vd_zjlsE7Sw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTIz/NjI1ODE3MS9waG90/by9oYXJ2YXJkLW1l/bW9yaWFsLWhhbGwu/anBnP3M9NjEyeDYx/MiZ3PTAmaz0yMCZj/PXl3RS1tWU1ONUZL/NF9wVXZqbzQyLUJP/Z21vMTg1OThTVjZv/TnBEVlMwQUk9",
        "https://imgs.search.brave.com/xxMER5mnfPJmX4CeX3E7Dzt0M7e_tKn67JwhEuu7LM0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTUz/NDc4OTgyL3Bob3Rv/L2dvaW5nLXRvLWNs/YXNzLmpwZz9zPTYx/Mng2MTImdz0wJms9/MjAmYz1taEtLNGtC/eTFZX2Q0MlVLaHNB/VTJKbzdLSVhDZUd6/Vkh4Z3hJeVIyTWxn/PQ",
        "https://imgs.search.brave.com/lNjCDK2DocIxcQiXWrrx54Y3w7phax4PwNKLIOXdMHw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzAyLzg3LzQ2LzMy/LzM2MF9GXzI4NzQ2/MzIwNF9La0Y4VjZs/Z2lWbHBsSU5XbU1k/R0liaWJ5OXlIUk5P/Yi5qcGc",
        "https://imgs.search.brave.com/IPr98duPyGaIsXhxhr5uGijEZe8NY9pPPgQ8M7dCUbw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTMy/MzQyMDczNy9waG90/by9hZXJpYWwtb3Zl/ci1ub3J0aC1jYXJv/bGluYS1jZW50cmFs/LXVuaXZlcnNpdHkt/aW4tdGhlLXNwcmlu/Zy5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9S2dOdWRIeDEt/RG5mN1BhWnByYzZM/Z2V2b3lqQ1V0MkxW/LWNhMktrRGNIMD0",
        "https://imgs.search.brave.com/cY1aBacTUAM2NxeVS1vgezbzB_KoDEDt47kfJEJmYZ8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAyMC8w/NS8xOC8yMi8xOC91/bml2ZXJzaXR5LTUx/ODg2MTBfMTI4MC5q/cGc",
        "https://imgs.search.brave.com/Mzmdz7ANla0Yr3Rl-YBYPUs_KFT-_ypg9VyDVKIn7yc/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAyLzgwLzIxLzIz/LzM2MF9GXzI4MDIx/MjMwNV9LZ1pkQ245/WjdXODR5dEV2Y1pW/MGlONmNpTTczY2Nx/bS5qcGc",
        "https://imgs.search.brave.com/XzwsLvgUN_PRL1j0ZpLOxQnWWDhwP5RPLFsDpVkbsCw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAyMC8w/Mi8wNi8yMC80OC91/bmktNDgyNTQ3MV82/NDAuanBn",
        "https://imgs.search.brave.com/dRJ5bVAQNoF1onaiITaTFgvT67F1hiJJQFK90_M5CL8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/aW1hZ2VzLm94LmFj/LnVrL2ltYWdlcy9p/bmRleC1jYXJkcy9E/RVRBSUwyMDIyMTAx/NC5qcGc",
        "https://imgs.search.brave.com/5X0WblWaujW4nvODNjuYELJXMxePtKuAS5Q74RPms7Q/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAyLzU0LzQyLzQx/LzM2MF9GXzI1NDQy/NDExNV9keDFrNDNh/cVhGN2RHVzQyRWxL/MFF3RFNCQlNlRVc4/aC5qcGc",
        "https://imgs.search.brave.com/AbR3i75IZTz27DHiPIPEKliLqi0u2TUq85XSvzd_Rfw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzA0LzYwLzA4LzUz/LzM2MF9GXzQ2MDA4/NTM2NV9SWDJxU3Y2/enhoeWFiRVBaaTVB/ejh5YUtycWdFS2dD/dC5qcGc",
        "https://imgs.search.brave.com/yi3yHyx_AIX9iB0eGgWdjjNVe2C2hRfWElV51_f-QJQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/cGl4YWJheS5jb20v/cGhvdG8vMjAxOS8x/MC8yMi8xNy8xNi9z/aGFuZ2hhaS1qaWFv/LXRvbmctdW5pdmVy/c2l0eS00NTY5MjYy/XzY0MC5qcGc",
        "https://imgs.search.brave.com/8mqFRdAPDkCJBy_Faj2cEC9jneNhaQJMr6m76O7_rjk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTQ1/Njc0OTE5NC9waG90/by9jb2xsZWdlLXN0/dWRlbnRzLWFycml2/aW5nLWZvci1uaWdo/dC1zY2hvb2wuanBn/P3M9NjEyeDYxMiZ3/PTAmaz0yMCZjPXF6/N1JNZGc0Y2dpb1dZ/dUtJUTByNGlaN2l0/SWJUcmhPUlRjci15/MEsyUms9",
        "https://imgs.search.brave.com/dQiwgDS8-U6Sk_uS4owK4PyHf7df_UMI8tyktbE5G8w/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTc3/OTA3MDc1Ni9waG90/by90d28tdW5pdmVy/c2l0eS1zdHVkZW50/cy13YWxrLWRvd24t/Y2FtcHVzLXN0YWly/cy5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9TjdkMl82X2Fv/UFJlSmQ5YjZmVU1H/OXhXd0VqLXlYOVVH/LXFqZGNJeHdzMD0",
        "https://imgs.search.brave.com/gAq6EpBUWXCgReM-1hfcOyQuNY1sI_dfZFlk0k2AGAk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMTIx/NjYzNzYzMi9waG90/by9jb2xsZWdlLXN0/dWRlbnRzLWRlc2Nl/bmQtaW5kb29yLXN0/YWlyY2FzZS5qcGc_/cz02MTJ4NjEyJnc9/MCZrPTIwJmM9bXFy/YV83VlVab1FpRlAw/QVg4d2NPZ3N3bWtZ/U05pMUhXaURxVFlj/OUJkcz0",
        "https://imgs.search.brave.com/oiTKECqsnClqb3YknRNVG-x3hhQ0ulMC8zb2ZMl2tJQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvMjEy/MjE0ODM0OS9waG90/by93cml0aW5nLWFu/LWV4YW0tYXQtdGhl/LXVuaXZlcnNpdHku/anBnP3M9NjEyeDYx/MiZ3PTAmaz0yMCZj/PUxnVnpMY2RfY3hO/RFFyb2xaRkZxZzdB/SVFuVGRfeEJydmRX/ZnItZVZvSzg9",

    ]

    universities = []
    for i in range(n):
        name = fake.company()
        location = fake.city()
        # Cycle through the list of URLs for logo and banner.
        logo_url = image_urls[i % len(image_urls)]
        banner_url = image_urls[i % len(image_urls)]
        description = fake.text()
        website = fake.url()

        cursor.execute(
            """
            INSERT INTO universities (UniversityName, Location, LogoURL, BannerURL, Description, WebsiteURL)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE UniversityID = UniversityID
            """,
            (name, location, logo_url, banner_url, description, website),
        )

        universities.append(cursor.lastrowid)

    conn.commit()
    return universities


def insert_roles():
    roles = [
        ("Spectator", "Track tournament progress and learn about participating universities."),
        ("Super Admin", "Grant permissions to any user as necessary (primarily Aardvark Games employees)"),
        ("Aardvark Games Employee", "Perform any other roles as necessary as well as view reports, logs, support tickets, etc."),
        ("Marketing Staff", "Post updates, manage university pages, review content tickets (approval of player/team profile pictures and biographies/descriptions)."),
        ("Tournament Facilitator", "Record match results, enforce rules."),
        ("Team Captain", "Register teams, manage members, post updates, and promote someone else on the team to be team leader."),
        ("Student/Player", "Join teams, leave teams, start a team, and view schedules."),
        ("College Admin", "Manage university related operations. Oversees student registations, apporve teams, and handle admin tasks for tournaments and events"),
    ]

    role_ids = []

    for role_name, description in roles:
        cursor.execute(
            """
            INSERT INTO roles (RoleName, Description)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE RoleName=VALUES(RoleName)
            """,
            (role_name, description),
        )

    conn.commit()
    
    cursor.execute("SELECT RoleID FROM roles")
    role_ids = [row[0] for row in cursor.fetchall()]
    
    return role_ids


def insert_users(n=200, university_ids=[], role_ids=[]):
    users = []
    generated_usernames = set()
    generated_emails = set()
    generated_uids = set()

    for _ in range(n):
        while True:
            username = fake.user_name()
            email = fake.email()
            firebase_uid = fake.uuid4()

            if (
                username not in generated_usernames
                and email not in generated_emails
                and firebase_uid not in generated_uids
            ):
                generated_usernames.add(username)
                generated_emails.add(email)
                generated_uids.add(firebase_uid)
                break

        cursor.execute(
            """
            INSERT INTO users (FirstName, LastName, Username, Email, FirebaseUID, ProfileImageURL, Bio, Paid, RoleID, UniversityID, IsValidated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                fake.first_name(),
                fake.last_name(),
                username,
                email,
                firebase_uid,
                fake.image_url(),
                fake.sentence(),
                random.choice([True, False]),
                random.choice(role_ids),
                random.choice(university_ids),
                random.choice([True, False]),
            ),
        )
        users.append(cursor.lastrowid)

    conn.commit()
    return users


def insert_teams(university_ids=[], user_ids=[], teams_per_university=4):
    teams = []
    generated_team_names = set()
    for uni in university_ids:
        for _ in range(teams_per_university):
            while True:
                team_name = fake.word().capitalize() + " Team"
                if team_name not in generated_team_names:
                    generated_team_names.add(team_name)
                    break
            cursor.execute(
                """
                INSERT INTO teams (UniversityID, TeamName, ProfileImageURL, Description, TeamLeaderID, IsApproved)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    uni,
                    team_name,
                    fake.image_url(),
                    fake.text(),
                    random.choice(user_ids),
                    random.choice([True, False]),
                ),
            )
            teams.append(cursor.lastrowid)
    conn.commit()
    return teams



def insert_tournaments(n=20):
    tournaments = []
    generated_tournament_names = set()

    for _ in range(n):
        while True:
            tournament_name = fake.word().capitalize() + " Tournament"
            if tournament_name not in generated_tournament_names:
                generated_tournament_names.add(tournament_name)
                break

        start_date = fake.date_this_year()
        end_date = start_date + timedelta(days=random.randint(1, 10))
        status = random.choice(["Active", "Completed", "Cancelled", "Upcoming"])
        location = fake.city()

        cursor.execute(
            """
            INSERT INTO tournaments (TournamentName, StartDate, EndDate, Status, Location)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (tournament_name, start_date, end_date, status, location),
        )

        tournaments.append(cursor.lastrowid)

    conn.commit()
    return tournaments


def insert_matches(n=100, tournaments=[], teams=[]):
    for _ in range(n):
        tournament_id = random.choice(tournaments) if tournaments else None
        team1, team2 = random.sample(teams, 2) if len(teams) > 1 else (None, None)
        score1, score2 = random.randint(0, 10), random.randint(0, 10)
        winner = team1 if score1 > score2 else team2 if score2 > score1 else None
        match_time = fake.date_time_this_year()

        cursor.execute(
            """
            INSERT INTO matches (TournamentID, Team1ID, Team2ID, Score1, Score2, WinnerID, MatchTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (tournament_id, team1, team2, score1, score2, winner, match_time),
        )

    conn.commit()


def insert_tickets(n=80, users=[]):
    ticket_types = ["Bug Report", "User Report", "General Inquiry", "Approval Request"]
    statuses = ["Open", "In Progress", "Closed"]

    for _ in range(n):
        user_id = random.choice(users) if users else None
        subject = fake.sentence()
        description = fake.text()
        status = random.choice(statuses)
        ticket_type = random.choice(ticket_types)
        reported_user = random.choice(users) if random.random() > 0.5 else None

        cursor.execute(
            """
            INSERT INTO tickets (UserID, Subject, Description, Status, TicketType, ReportedUserID)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, subject, description, status, ticket_type, reported_user),
        )

    conn.commit()


#tournamentParticipants now uses TeamID and additional columns
def insert_tournament_participants(users, tournaments):
    if not users or not tournaments:
        print("Error: No users or tournaments available.")
        return

    #build a map of UserID to TeamID for users that have a team
    cursor.execute("SELECT UserID, TeamID FROM users WHERE TeamID IS NOT NULL")
    user_team_map = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.execute("SELECT TeamID FROM teams")
    all_teams = [row[0] for row in cursor.fetchall()]
    if not all_teams:
        print("No teams available.")
        return

    for tournament_id in tournaments:
        selected_users = random.sample(users, min(len(users), random.randint(5, 20)))
        team_ids = set()
        for user_id in selected_users:
            team_id = user_team_map.get(user_id)
            if team_id is None:
                team_id = random.choice(all_teams)
            team_ids.add(team_id)
        team_ids = list(team_ids)
        num_teams = len(team_ids)
        bracket_size = 2 ** math.ceil(math.log2(num_teams)) if num_teams > 0 else 0
        num_byes = bracket_size - num_teams

        random.shuffle(team_ids)
      
        bracket_data = []
        for index, team_id in enumerate(team_ids):
            if index < num_byes:
                round_number = 2  
            else:
                round_number = 1
            bracket_side = 'left' if index % 2 == 0 else 'right'
            bracket_data.append({
                'team_id': team_id,
                'round': round_number,
                'byes': 1 if round_number == 2 else 0,
                'status': 'active',
                'bracket_side': bracket_side,
                'next_match_id': None  
            })

        for entry in bracket_data:
            cursor.execute(
                """
                INSERT INTO tournament_participants (TournamentID, TeamID, Round, Byes, Status, BracketSide, NextMatchID)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (tournament_id, entry['team_id'], entry['round'], entry['byes'], entry['status'], entry['bracket_side'], entry['next_match_id'])
            )

    conn.commit()

def insert_tournament_facilitators(users, tournaments):
    if not users or not tournaments:
        print("Error: No users or tournaments available.")
        return

    for tournament_id in tournaments:
        facilitators = random.sample(users, min(len(users), random.randint(1, 5)))
        for user_id in facilitators:
            cursor.execute(
                """
                INSERT INTO tournament_facilitators (TournamentID, UserID)
                VALUES (%s, %s)
                """,
                (tournament_id, user_id),
            )

    conn.commit()


def simulate_tournament_bracket(tournament_id):
    #fetch participating teams from TournamentParticipants for the given tournament that are still active.
    cursor.execute("SELECT TeamID FROM tournament_participants WHERE TournamentID = %s AND Status = 'active'", (tournament_id,))
    rows = cursor.fetchall()
    teams = [row[0] for row in rows]
    if not teams:
        print(f"Tournament {tournament_id} has no active participating teams.")
        return

    #print(f"Simulating bracket for Tournament {tournament_id} with teams: {teams}")
    round_number = 1
    #set a base start date for the tournament
    base_datetime = datetime.now() + timedelta(days=random.randint(1, 5))

    while len(teams) > 1:
        #print(f"--- Round {round_number} ---")
        next_round = []
        #if odd number, give a bye to the first team.
        if len(teams) % 2 != 0:
            bye_team = teams.pop(0)
            next_round.append(bye_team)
            #print(f"Team {bye_team} receives a bye to next round.")
        for i in range(0, len(teams), 2):
            t1 = teams[i]
            t2 = teams[i+1]
            score1 = random.randint(0, 10)
            score2 = random.randint(0, 10)
            if score1 == score2:
                winner = random.choice([t1, t2])
            else:
                winner = t1 if score1 > score2 else t2
            loser = t1 if winner == t2 else t2
            # calculate a match datetime
            match_date = base_datetime + timedelta(days=round_number - 1)
            match_hour = random.randint(10, 20)
            match_minute = random.randint(0, 59)
            match_datetime = match_date.replace(hour=match_hour, minute=match_minute, second=0, microsecond=0)
            cursor.execute(
                """
                INSERT INTO matches (TournamentID, Team1ID, Team2ID, Score1, Score2, WinnerID, MatchTime)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (tournament_id, t1, t2, score1, score2, winner, match_datetime)
            )
            match_id = cursor.lastrowid
            #update the winning team's TournamentParticipants record with NextMatchID
            cursor.execute(
                "UPDATE tournament_participants SET NextMatchID = %s WHERE TournamentID = %s AND TeamID = %s",
                (match_id, tournament_id, winner)
            )
            #update the losing team's TournamentParticipants record to 'lost'
            cursor.execute(
                "UPDATE tournament_participants SET Status = 'lost' WHERE TournamentID = %s AND TeamID = %s",
                (tournament_id, loser)
            )
            #print(f"Match: {t1} vs {t2} | Score: {score1}-{score2} | Winner: {winner} (Match ID: {match_id}) at {match_datetime.strftime('%Y-%m-%d %H:%M')}")
            next_round.append(winner)
        conn.commit()
        teams = next_round
        round_number += 1

    # final winner
    champion = teams[0]
    cursor.execute(
        "UPDATE tournament_participants SET Status = 'winner' WHERE TournamentID = %s AND TeamID = %s",
        (tournament_id, champion)
    )
    conn.commit()
    #print(f"Tournament {tournament_id} Champion: {champion}")


def assign_users_to_teams(users, teams):
    if not users or not teams:
        print("Error: No users or teams available.")
        return

    for user_id in users:
        team_id = random.choice(teams)  # Pick a random existing team
        cursor.execute(
            """
            UPDATE users SET TeamID = %s WHERE UserID = %s
            """,
            (team_id, user_id),
        )

    conn.commit()


# Insert Data
roles = insert_roles()
if(len(sys.argv) > 1 and sys.argv[1] == "demo"):
    universities = insert_universities()
    users = insert_users(university_ids=universities, role_ids=roles)
    teams = insert_teams(university_ids=universities, user_ids=users)
    tournaments = insert_tournaments()
    #insert_matches(tournaments=tournaments, teams=teams)
    insert_tickets(users=users)
    insert_tournament_participants(users=users, tournaments=tournaments)
    insert_tournament_facilitators(users=users, tournaments=tournaments)

    assign_users_to_teams(users=users, teams=teams)

    # Simulate a complete tournament bracket for each tournament (single elimination, randomized number of teams)
    for t in tournaments:
        simulate_tournament_bracket(t)
    print("Dummy data inserted and tournament brackets simulated successfully!")

cursor.close()
conn.close()
print("Data inserted successfully!")
