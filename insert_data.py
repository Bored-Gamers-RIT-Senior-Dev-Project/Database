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
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
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
        
        cursor.execute("""
            INSERT INTO Universities (UniversityName, Location, LogoURL, BannerURL, Description, WebsiteURL)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, location, logo_url, banner_url, description, website))
        
        universities.append(cursor.lastrowid)
    
    conn.commit()
    return universities


def insert_roles():
    roles = ["Super Admin", "University Admin", "Student"]
    role_ids = []
    
    for role in roles:
        cursor.execute("""
            INSERT INTO Roles (RoleName, Description)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE RoleID=RoleID
        """, (role, f"{role} role in the system"))
        
        cursor.execute("SELECT RoleID FROM Roles WHERE RoleName = %s", (role,))
        role_ids.append(cursor.fetchone()[0])
    
    conn.commit()
    return role_ids

def insert_users(n=150, university_ids=[], role_ids=[]):
    users = []
    for _ in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = fake.user_name()
        email = fake.email()
        firebase_uid = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        profile_img = fake.image_url()
        bio = fake.sentence()
        paid = random.choice([True, False])
        university_id = random.choice(university_ids) if university_ids else None
        role_id = random.choice(role_ids) if role_ids else 3  # Default to 'Student'
        is_validated = random.choice([True, False])

        cursor.execute("""
            INSERT INTO Users (FirstName, LastName, Username, Email, FirebaseUID, ProfileImageURL, Bio, Paid, RoleID, UniversityID, IsValidated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, username, email, firebase_uid, profile_img, bio, paid, role_id, university_id, is_validated))
        
        users.append(cursor.lastrowid)
    
    conn.commit()
    return users

def insert_teams(n=50, university_ids=[], user_ids=[]):
    teams = []
    for _ in range(n):
        university_id = random.choice(university_ids) if university_ids else None
        team_name = fake.word().capitalize() + " Team"
        profile_img = fake.image_url()
        description = fake.text()
        team_leader = random.choice(user_ids) if user_ids else None
        is_approved = random.choice([True, False])

        cursor.execute("""
            INSERT INTO Teams (UniversityID, TeamName, ProfileImageURL, Description, TeamLeaderID, IsApproved)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (university_id, team_name, profile_img, description, team_leader, is_approved))
        
        teams.append(cursor.lastrowid)

    conn.commit()
    return teams

def insert_tournaments(n=20):
    tournaments = []
    for _ in range(n):
        name = fake.word().capitalize() + " Tournament"
        start_date = fake.date_this_year()
        end_date = start_date + timedelta(days=random.randint(1, 10))
        status = random.choice(["Active", "Completed", "Cancelled", "Upcoming"])
        location = fake.city()

        cursor.execute("""
            INSERT INTO Tournaments (TournamentName, StartDate, EndDate, Status, Location)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, start_date, end_date, status, location))
        
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

        cursor.execute("""
            INSERT INTO Matches (TournamentID, Team1ID, Team2ID, Score1, Score2, WinnerID, MatchTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (tournament_id, team1, team2, score1, score2, winner, match_time))
    
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

        cursor.execute("""
            INSERT INTO Tickets (UserID, Subject, Description, Status, TicketType, ReportedUserID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, subject, description, status, ticket_type, reported_user))
    
    conn.commit()


universities = insert_universities()
roles = insert_roles()
users = insert_users(university_ids=universities, role_ids=roles)
teams = insert_teams(university_ids=universities, user_ids=users)
tournaments = insert_tournaments()
insert_matches(tournaments=tournaments, teams=teams)
insert_tickets(users=users)


cursor.close()
conn.close()

print("Dummy data inserted successfully!")
