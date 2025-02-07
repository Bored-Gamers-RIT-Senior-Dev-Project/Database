#!/bin/bash

# Database details
MYSQL_USER="root"
MYSQL_HOST="localhost"
MYSQL_DB="BoardGame"

SQL_FILE="$(dirname "$0")/create_database.sql"

read -sp "Enter your database password: " MYSQL_PASSWORD
echo

# Check for SQL file 
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file $SQL_FILE not found!"
    exit 1
fi

# Run create_databse.sql
echo "Resetting and recreating the database..."
mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -h $MYSQL_HOST < "$SQL_FILE"

# Check for errors
if [ $? -eq 0 ]; then
    echo "Database reset and schema applied successfully!"
else
    echo "There was an error while applying the database update."
fi
