import sqlite3
from datetime import datetime

DATABASE_NAME = "TakeYourJourney.db"


# Connect to the database
def connect_to_database():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


# Check if the database exists and create it if not
def check_if_database_exists():
    try:
        conn = connect_to_database()
        conn.close()
        print("Database already exists.")
    except sqlite3.Error:
        print("Database does not exist, creating a new one...")
        create_database()


# Create the database
def create_database():
    conn = connect_to_database()
    conn.close()
    print("Database created successfully.")


# Check for the existence of the user table and the presence of the user in it
def check_user_in_user_table(user_id, user_name):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Check if the users table exists
    cursor.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users';"
    )
    table_exists = cursor.fetchone()[0]

    if not table_exists:
        # If the table does not exist, create it
        cursor.execute(
            "CREATE TABLE users (user_id INTEGER PRIMARY KEY, user_name TEXT, codename TEXT, registration_date TEXT, profile_count INTEGER);"
        )
        print("User table created.")
        conn.commit()

    # Check if the user exists in the table
    cursor.execute(
        "SELECT count(*) FROM users WHERE user_id = ? AND user_name = ?",
        (user_id, user_name),
    )
    user_exists = cursor.fetchone()[0]

    if user_exists:
        return True
    else:
        return False


# Returns a list of all user-related tables
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


# Add a user to the database
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
        CREATE TABLE IF NOT EXISTS {visitings_table_name} (
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


# Create a profile for a user
def profile_creating(user_id, profile_nametag):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Name of the profile table
    profile_table_name = f"{user_id}-{profile_nametag}"

    # Create profile table with the specified fields
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {profile_table_name} (
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

    # Update user's profile count
    cursor.execute(
        """
        UPDATE users 
        SET profile_count = profile_count + 1 
        WHERE user_id = ?
        """,
        (user_id,),
    )

    # Insert new profile into user_profiles table
    cursor.execute(
        """
        INSERT INTO user_profiles (user_id, profile_name, profile_photo, date_added) 
        VALUES (?, ?, ?, ?)
        """,
        (user_id, profile_nametag, None, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )

    conn.commit()
    conn.close()
    print(f"Profile table {profile_table_name} created for user {user_id}.")


# Check if the database exists when this module is imported
check_if_database_exists()
