#!/usr/bin/env python3
import os
import platform
import subprocess
import getpass
import mysql.connector

def get_mysql_config_path():
    """Determine MySQL config file location based on OS."""
    if platform.system() == "Windows":
        # Check common Windows MySQL installation paths
        base_paths = [
            r"C:\ProgramData\MySQL",
            r"C:\Program Files\MySQL"
        ]
        for base in base_paths:
            if os.path.exists(base):
                for root, dirs, files in os.walk(base):
                    for file in files:
                        if file.lower() == "my.ini":
                            return os.path.join(root, file)
        # Fallback: change 'X.X' to your installed version if needed
        return r"C:\Program Files\MySQL\MySQL Server X.X\my.ini"
    else:
        # Linux/macOS common config file paths
        possible_paths = ["/etc/mysql/my.cnf", "/etc/my.cnf", "/usr/local/mysql/my.cnf"]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    return None

def check_lower_case_setting():
    """Check if lower_case_table_names is set correctly using MySQL connector."""
    mysql_password = getpass.getpass("Enter your database password for MySQL check: ")
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="mysql"
        )
        cursor = conn.cursor()
        cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names';")
        result = cursor.fetchone()
        conn.close()
        if result:
            current_value = int(result[1])
            print(f"Current lower_case_table_names value: {current_value}")
            return current_value, mysql_password
        else:
            return None, mysql_password
    except mysql.connector.Error as e:
        print(f"Error checking MySQL setting: {e}")
        return None, mysql_password

def update_mysql_config():
    """Modify the MySQL config file to set lower_case_table_names=1."""
    config_path = get_mysql_config_path()
    if not config_path:
        print("Error: MySQL config file not found!")
        return False

    try:
        with open(config_path, "r") as file:
            lines = file.readlines()

        found = False
        for i, line in enumerate(lines):
            if line.strip().startswith("lower_case_table_names"):
                lines[i] = "lower_case_table_names=1\n"
                found = True
                break

        if not found:
            # Ensure [mysqld] section exists; if not, add it.
            if not any(line.strip() == "[mysqld]" for line in lines):
                lines.append("\n[mysqld]\n")
            lines.append("lower_case_table_names=1\n")

        with open(config_path, "w") as file:
            file.writelines(lines)

        print(f"Updated {config_path} successfully.")
        return True
    except Exception as e:
        print(f"Error updating MySQL config: {e}")
        return False

def restart_mysql():
    """Restart MySQL service based on OS."""
    try:
        if platform.system() == "Windows":
            subprocess.run(["net", "stop", "mysql"], shell=True, check=True)
            subprocess.run(["net", "start", "mysql"], shell=True, check=True)
        else:
            subprocess.run(["sudo", "systemctl", "restart", "mysql"], check=True)
        print("MySQL service restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting MySQL: {e}")

def reset_database(mysql_password):
    """Runs the SQL script to reset the database."""
    MYSQL_USER = "root"
    MYSQL_HOST = "localhost"
    MYSQL_DB = "BoardGame"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(script_dir, "create_database.sql")

    if not os.path.isfile(sql_file):
        print(f"Error: SQL file {sql_file} not found!")
        return

    print("Resetting and recreating the database...")

    try:
        subprocess.run(
            [
                "mysql",
                "-u", MYSQL_USER,
                f"-p{mysql_password}",
                "-h", MYSQL_HOST,
                MYSQL_DB,
            ],
            stdin=open(sql_file, "r"),
            check=True,
            text=True,
        )
        print("Database reset and schema applied successfully!")
    except subprocess.CalledProcessError:
        print("Error applying the database update.")

def main():
    current_setting, mysql_password = check_lower_case_setting()
    if current_setting != 1:
        print("Updating MySQL configuration to set lower_case_table_names=1...")
        if update_mysql_config():
            restart_mysql()
        else:
            print("Failed to update MySQL configuration. Exiting.")
            return
    else:
        print("lower_case_table_names is already set to 1.")

    reset_database(mysql_password)

if __name__ == "__main__":
    main()
