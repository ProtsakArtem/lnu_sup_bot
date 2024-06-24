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