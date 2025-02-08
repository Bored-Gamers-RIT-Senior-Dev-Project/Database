import os
import subprocess
import getpass


def main():
    # Database details
    MYSQL_USER = "root"
    MYSQL_HOST = "localhost"
    MYSQL_DB = "BoardGame"

    # SQL file path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    SQL_FILE = os.path.join(script_dir, "create_database.sql")

    # Prompt for password
    MYSQL_PASSWORD = getpass.getpass("Enter your database password: ")

    # Check for SQL file
    if not os.path.isfile(SQL_FILE):
        print(f"Error: SQL file {SQL_FILE} not found!")
        return

    # Run the SQL file
    print("Resetting and recreating the database...")

    try:
        result = subprocess.run(
            [
                "mysql",
                "-u",
                MYSQL_USER,
                f"-p{MYSQL_PASSWORD}",
                "-h",
                MYSQL_HOST,
                MYSQL_DB,
            ],
            stdin=open(SQL_FILE, "r"),
            check=True,
            text=True,
        )
        print("Database reset and schema applied successfully!")
    except subprocess.CalledProcessError:
        print("There was an error while applying the database update.")


if __name__ == "__main__":
    main()
