import sqlite3 as sql

def insertDetails(email, first_name, last_name, password):
    conn = sql.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_details (email, first_name, last_name, password) VALUES (?, ?, ?, ?)",
        (email, first_name, last_name, password)
    )
    conn.commit()
    conn.close()

def check_credentials(email, password):
    conn = sql.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user_details WHERE email = ? AND password = ?", (email, password)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_dict = {
            "id": user[0],
            "email": user[1],
            "first_name": user[2],
            "last_name": user[3],
            "password": user[4]
        }
        return user_dict
    return None