import sqlite3
from datetime import datetime

DATABASE_NAME = "TakeYourJourney.db"


# connect to the database
def connect_to_database():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


# check if the database exists and create it if not
def check_if_database_exists():
    try:
        conn = connect_to_database()
        conn.close()
        print("Database already exists.")
    except sqlite3.Error:
        print("Database does not exist, creating a new one...")
        create_database()

    # ensure all necessary tables are created
    create_user_table()


# create the database
def create_database():
    conn = connect_to_database()
    conn.close()
    print("Database created successfully.")


# create the users table if it does not exist
def create_user_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            codename TEXT,
            registration_date TEXT,
            profile_count INTEGER
        )
        """
    )
    conn.commit()
    conn.close()
    print("User table checked/created successfully.")


# create the user_profiles table if it does not exist
def create_user_profiles_table(user_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    user_profile = f"{user_id}_profiles"
    
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{user_profile}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            profile_name TEXT,
            profile_photo BLOB,
            date_added TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
        """
    )
    conn.commit()
    conn.close()
    print("User profiles table checked/created successfully.")


# check for the existence of the user in the user table
def check_user_in_user_table(user_id, user_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if the user exists in the table
    cursor.execute(
        "SELECT count(*) FROM users WHERE user_id = ? AND user_name = ?",
        (user_id, user_name),
    )
    user_exists = cursor.fetchone()[0]

    conn.close()
    
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
    conn.close()
    return table_names


# add a user to the database
def add_user(user_id, user_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # generate codename without padding
    codename = f"{user_id}-{user_name}"

    # get current date
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # profile count starts at 0 for new users
    profile_count = 0

    # add user to the users table
    cursor.execute(
        "INSERT INTO users (user_id, user_name, codename, registration_date, profile_count) VALUES (?, ?, ?, ?, ?)",
        (user_id, user_name, codename, registration_date, profile_count),
    )

    # create a related table for visitings
    visitings_table_name = f"{user_id}_visitings"
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{visitings_table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visited_place TEXT,
            term_from TEXT,
            term_to TEXT,
            transport_mode TEXT,
            travel_cost REAL,
            accommodation_cost REAL,
            accommodation_link TEXT,
            spent_amount REAL,
            interesting_places TEXT,
            date_added TEXT
        )
    """
    )

    conn.commit()
    conn.close()
    print(
        f"user {codename} added successfully and table {visitings_table_name} created."
    )


# create a profile for a user
def profile_creating(user_id, profile_nametag):
    conn = connect_to_database()
    cursor = conn.cursor()

    # name of the profile table
    profile_table_name = f"{user_id}-{profile_nametag}"

    # create profile table with the specified fields
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS "{profile_table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_name TEXT,
            profile_photo BLOB,
            avg_flight_cost_3_months REAL,
            cheapest_ticket REAL,
            standard_accommodation REAL,
            period_accommodation REAL,
            visit_count INTEGER DEFAULT 0,
            date_added TEXT
        )
    """
    )

    # update user's profile count
    cursor.execute(
        """
        UPDATE users 
        SET profile_count = profile_count + 1 
        WHERE user_id = ?
        """,
        (user_id,),
    )

    # insert new profile into user(user_id)_profiles table
    user_profile = f"{user_id}_profiles"
    cursor.execute(
        f"""
        INSERT INTO "{user_profile}" (user_id, profile_name, profile_photo, date_added) 
        VALUES (?, ?, ?, ?)
        """,
        (user_id, profile_nametag, None, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )

    conn.commit()
    conn.close()
    print(f"Profile table {profile_table_name} created for user {user_id}.")


# check if the database exists when this module is imported
check_if_database_exists()
