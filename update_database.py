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
    sql_file = os.path.join(script_dir, "create_database.sql")

    # Prompt for password
    mysql_password = getpass.getpass("Enter your database password: ")

    # Check for SQL file
    if not os.path.isfile(sql_file):
        print(f"Error: SQL file {sql_file} not found!")
        return

    # Run the SQL file
    print("Resetting and recreating the database...")

    try:
        result = subprocess.run(
            [
                "mysql",
                "-u",
                MYSQL_USER,
                f"-p{mysql_password}",
                "-h",
                MYSQL_HOST,
                MYSQL_DB,
            ],
            stdin=open(sql_file, "r"),
            check=True,
            text=True,
        )
        if result == 0:
            print("Database reset and schema applied successfully!")
        else:
            print("There was an error while applying the database update.")
    except subprocess.CalledProcessError:
        print("There was an error while applying the database update.")


if __name__ == "__main__":
    main()
