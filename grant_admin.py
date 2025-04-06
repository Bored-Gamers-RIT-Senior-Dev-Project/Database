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

# Some help from copilot catching errors since I haven't worked in python for a bit.
def grant_admin(email):
    print(f"Making {email} an admin...", end=" ")
    try:
        cursor.execute("UPDATE users SET RoleID = 2 WHERE Email = %s", (email,))
        if cursor.rowcount > 0:
            print("\033[92mSuccess!\033[0m")
        else:
            print("\033[93mFailed.\033[0m")
    except mysql.connector.Error as err:
        print(f"\033[91mError.\033[0m\n{err}")



email_list = sys.argv[1:]
for email in email_list:
    grant_admin(email)

conn.commit()
cursor.close()
conn.close()