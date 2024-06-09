import sqlite3

connection = sqlite3.connect('bot_father', check_same_thread=False)
cursor = connection.cursor()

# users_table_sql = '''
# DROP TABLE IF EXISTS users;
# CREATE TABLE IF NOT EXISTS users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     first_name TEXT,
#     chat_id BIGINT NOT NULL
# );
# '''
# cursor.executescript(users_table_sql)
#
#
# translations_sql = '''
# DROP TABLE IF EXISTS translations;
# CREATE TABLE IF NOT EXISTS translations(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     lang_from TEXT,
#     lang_to TEXT,
#     original_text TEXT,
#     translated_text TEXT,
#     user_id INTEGER REFERENCES users(id)
# );
# '''
# cursor.executescript(translations_sql)


def is_user_exists(chat_id):
    sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(sql, (chat_id,))
    user_id = cursor.fetchone()
    if not user_id:
        return False
    return True


def add_user(first_name, chat_id):
    sql = 'INSERT INTO users(first_name, chat_id) VALUES (?, ?)'
    if not is_user_exists(chat_id):
        cursor.execute(sql, (first_name, chat_id))
        connection.commit()


def add_translated(original_text, translator_text, lang_from, lang_to, chat_id):
    sql = 'INSERT INTO translations(original_text, translated_text, lang_from, lang_to, user_id) VALUES (?, ?, ?, ?, ?)'
    user_id_sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(user_id_sql, (chat_id,))
    user_id = cursor.fetchone()[0]
    cursor.execute(sql, (original_text, translator_text, lang_from, lang_to, user_id))
    connection.commit()

def history(chat_id):
    user_id_sql = 'SELECT id FROM users WHERE chat_id=?'
    cursor.execute(user_id_sql, (chat_id,))
    user_id = cursor.fetchone()[0]
    original_text = 'SELECT original_text FROM translations WHERE user_id=?'
    translate_text = 'SELECT translated_text FROM translations WHERE user_id=?'
    cursor.execute(original_text, (user_id,))
    original = cursor.fetchall()
    cursor.execute(translate_text, (user_id,))
    translate = cursor.fetchall()
    count = -1
    history_l = []
    for text in original:
        count += 1
        history_l.append(f'{text}-{translate[count]}\n')

    return history_l

