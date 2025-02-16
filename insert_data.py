#!/usr/bin/env python3
import mysql.connector
import random
import string
from datetime import datetime, timedelta
from faker import Faker
import getpass


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
    universities = []
    for _ in range(n):
        name = fake.company()
        location = fake.city()
        logo_url = fake.image_url()
        banner_url = fake.image_url()
        description = fake.text()
        website = fake.url()

        cursor.execute(
            """
            INSERT INTO Universities (UniversityName, Location, LogoURL, BannerURL, Description, WebsiteURL)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (name, location, logo_url, banner_url, description, website),
        )

        universities.append(cursor.lastrowid)

    conn.commit()
    return universities


# Added all user roles
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
            INSERT INTO Roles (RoleName, Description)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE RoleName=VALUES(RoleName)
        """,
            (role_name, description),
        )

    conn.commit()
    
    cursor.execute("SELECT RoleID FROM Roles")
    role_ids = [row[0] for row in cursor.fetchall()]

    #print("Roles retrieved:", role_ids) 
    
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
            INSERT INTO Users (FirstName, LastName, Username, Email, FirebaseUID, ProfileImageURL, Bio, Paid, RoleID, UniversityID, IsValidated)
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


def insert_teams(n=50, university_ids=[], user_ids=[]):
    teams = []
    generated_team_names = set()

    for _ in range(n):
        while True:
            team_name = fake.word().capitalize() + " Team"
            if team_name not in generated_team_names:
                generated_team_names.add(team_name)
                break

        cursor.execute(
            """
            INSERT INTO Teams (UniversityID, TeamName, ProfileImageURL, Description, TeamLeaderID, IsApproved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (
                random.choice(university_ids),
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
            INSERT INTO Tournaments (TournamentName, StartDate, EndDate, Status, Location)
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
            INSERT INTO Matches (TournamentID, Team1ID, Team2ID, Score1, Score2, WinnerID, MatchTime)
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
            INSERT INTO Tickets (UserID, Subject, Description, Status, TicketType, ReportedUserID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (user_id, subject, description, status, ticket_type, reported_user),
        )

    conn.commit()


# Forgot this table (whoops)
def insert_tournament_participants(users, tournaments):
    if not users or not tournaments:
        print("Error: No users or tournaments available.")
        return

    for tournament_id in tournaments:
        participants = random.sample(
            users, min(len(users), random.randint(5, 20))
        )  # Randomly assign 5-20 users per tournament
        for user_id in participants:
            cursor.execute(
                """
                INSERT INTO TournamentParticipants (TournamentID, UserID)
                VALUES (%s, %s)
                """,
                (tournament_id, user_id),
            )

    conn.commit()


# Assign users a team after both user and team has been created
def assign_users_to_teams(users, teams):

    if not users or not teams:
        print("Error: No users or teams available.")
        return

    for user_id in users:
        team_id = random.choice(teams)  # Pick a random existing team
        cursor.execute(
            """
            UPDATE Users SET TeamID = %s WHERE UserID = %s
        """,
            (team_id, user_id),
        )

    conn.commit()


# Insert Data
universities = insert_universities()
roles = insert_roles()
users = insert_users(university_ids=universities, role_ids=roles)
teams = insert_teams(university_ids=universities, user_ids=users)
tournaments = insert_tournaments()
insert_matches(tournaments=tournaments, teams=teams)
insert_tickets(users=users)
insert_tournament_participants(users=users, tournaments=tournaments)

assign_users_to_teams(users=users, teams=teams)


cursor.close()
conn.close()

print("Dummy data inserted successfully!")
