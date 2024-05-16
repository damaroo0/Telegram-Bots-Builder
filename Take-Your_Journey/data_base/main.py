# data_base/main.py

import sqlite3
import os


#
def check_if_database_existas():
    if os.path.exists("TakeYourJourney.db"):
        return True
    else:
        create_database()
        return True


def create_database() -> None:
    conn = sqlite3.connect("TakeYourJourney.db")
    conn.close()


#
def check_user_in_database(user_id, user_name):
    table_name = f"{user_id}-{user_name}"
    user_table_template = "()"

    conn = sqlite3.connect("TakeYourJourney.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    existing_table = cursor.fetchone()
    
    if existing_table:
        return True
    else:
        return False
    
    conn.close()
