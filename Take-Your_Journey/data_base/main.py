# data_base/main.py

import sqlite3

from datetime import datetime

DATABASE_NAME = "TakeYourJourney.db"


# connect to the database
def connect_to_database():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


# check if the database exists and create if not
def check_if_database_exists():
    try:
        conn = connect_to_database()
        conn.close()
        print("database already exists.")
    except sqlite3.Error:
        print("database does not exist, creating a new one...")
        create_database()


# create the database
def create_database():
    conn = connect_to_database()
    conn.close()
    print("database created successfully.")


# check for the existence of the user table and the presence of the user in it
def check_user_in_user_table(user_id, user_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # check if the users table exists
    cursor.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users';"
    )
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # if the table does not exist, create it
        cursor.execute(
            "CREATE TABLE users (user_id INTEGER PRIMARY KEY, user_name TEXT, codename TEXT, registration_date TEXT, profile_count INTEGER);"
        )
        print("User table created.")
        conn.commit()


    # check if the user exists in the table
    cursor.execute(
        "SELECT count(*) FROM users WHERE user_id = ? AND user_name = ?",
        (user_id, user_name),
    )
    user_exists = cursor.fetchone()[0]

    if user_exists:
        return True
    else:
        return False


# returns a list of all user-related tables
def user_profile(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?;",
        (f"user_id-{user_id}%",),
    )
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names


def add_user(user_id, user_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Generate codename without padding
    codename = f"{user_id}-{user_name}"

    # Get current date
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Profile count starts at 0 for new users
    profile_count = 0

    # Add user to the users table
    cursor.execute(
        "INSERT INTO users (user_id, user_name, codename, registration_date, profile_count) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_name, codename, registration_date, profile_count),
    )
    conn.commit()
    conn.close()
    print(f"User {codename} added successfully.")


def profile_creating(codename):
    pass
