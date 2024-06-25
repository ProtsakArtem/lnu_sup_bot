import sqlite3

all_text = {"start_text": "",
            "questions_text": "",
            "info_decanat_text": "",
            "zastup_info_text": "",
            "pay_req_text": "",
            "hurt_req_text": "",
            "help_links_text": "",
            "stud_orgs_text": "",
            "decan_time_text": ""
            }

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS info_text (
            key_text_name VARCHAR(100),
            text VARCHAR(4000)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            username VARCHAR(100),
            language_code VARCHAR(10),
            corrects INTEGER DEFAULT 0,
            incorrects INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sup_sessions (
            state_name VARCHAR(100),
            is_active INTEGER DEFAULT 0,
            user_id INTEGER DEFAULT 0,
            helper_id INTEGER DEFAULT 0,
            session_id VARCHAR(150)
        )
    ''')

    conn.commit()
    conn.close()


def fetch_all_text(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT key_text_name,text FROM info_text')

    data = cursor.fetchall()
    conn.close()
    return data


def set_text_variables():
    data = fetch_all_text('database.db')
    # start_text, questions_text, info_decanat_text, zastup_info_text, pay_req_text, hurt_req_text, start_text, help_links_text, decan_time_text = data
    # print(start_text, help_links_text)
    for row in data:
        all_text[row[0]] = row[1]

def set_user_in_help_session(user_id, session_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Convert session_id (which is a State object) to its string representation
    session_name = str(session_id)

    # Check if the record exists for this user_id
    cursor.execute("SELECT * FROM sup_sessions WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Update the session_id for the existing user
        cursor.execute("UPDATE sup_sessions SET session_id = ? WHERE user_id = ?", (session_name, user_id))
    else:
        # Insert a new record for the user
        cursor.execute("INSERT INTO sup_sessions (user_id, session_id) VALUES (?, ?)", (user_id, session_name))

    connection.commit()
    connection.close()


def set_helper_to_session(session_name, helper_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Виконуємо SQL-запит для безпечного вставлення даних
    cursor.execute("""
        UPDATE sup_sessions
        SET helper_id = ?
        WHERE session_id = ?
    """, (helper_id, session_name))  # Конвертуємо session_name в строку перед передачею

    conn.commit()
    conn.close()

def get_user_id_by_session(session_name):
    conn = sqlite3.connect("database.db")
    print(f"Getting user_id by session: {session_name}")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM sup_sessions
        WHERE session_id = ?
    """, (session_name,))  # Конвертуємо session_name в строку перед передачею

    result = cursor.fetchone()
    print(f"USERS DEBUG: {result}")
    user_id = result[0] if result else None

    conn.close()
    return user_id

def get_operator_id_by_session(session_name):
    conn = sqlite3.connect("database.db")
    print(f"Getting operator_id by session: {session_name}")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT helper_id
        FROM sup_sessions
        WHERE session_id = ?
    """, (session_name,))  # Конвертуємо session_name в строку перед передачею

    result = cursor.fetchone()
    print(f"OPERATORS DEBUG: {result}")
    operator_id = result[0] if result else None

    conn.close()
    return operator_id


def delete_session(session_name):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Debug: Print session_name to ensure it's correct
        print(f"Deleting session with session_id: {session_name}")

        cursor.execute("""
            DELETE FROM sup_sessions
            WHERE session_id = ?
        """, (session_name,))  # Ensure session_name matches the type in the database

        # Check the number of rows affected
        rows_affected = cursor.rowcount

        conn.commit()

        # Debug: Print the number of rows affected
        if rows_affected > 0:
            print(f"Successfully deleted {rows_affected} session(s).")
        else:
            print("No sessions were deleted. Please check the session_id.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

