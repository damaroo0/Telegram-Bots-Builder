# data_base/main.py

import sqlite3

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
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()[0]
    if table_exists:
        cursor.execute("SELECT count(*) FROM users WHERE user_id = ? AND user_name = ?", (user_id, user_name))
        user_exists = cursor.fetchone()[0]
        if user_exists:
            return True
        else:
            return False
    else:
        print("user table does not exist.")
        return False

# returns a list of all user-related tables
def user_profile(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?;", (f"user_id-{user_id}%",))
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names
