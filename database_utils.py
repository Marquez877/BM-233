import sqlite3

db_path = 'casino.db'


def get_db_connection():
    """Получение соединения с базой данных"""
    return sqlite3.connect(db_path)


def init_db():
    """Инициализация базы данных: создание таблицы, если она не существует"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS casino_users (
            chat_id INTEGER PRIMARY KEY,
            first_name TEXT,
            balance INTEGER DEFAULT 1000
        )
    ''')
    connection.commit()
    connection.close()


def add_user(chat_id, first_name):
    """Добавление нового пользователя в базу данных"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM casino_users WHERE chat_id = ?', (chat_id,))
        user = cursor.fetchone()
        if not user:
            cursor.execute(
                'INSERT INTO casino_users (chat_id, first_name, balance) VALUES (?, ?, ?)',
                (chat_id, first_name, 1000)
            )
            connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        connection.close()


def get_balance(chat_id):
    """Получение баланса пользователя по chat_id"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM casino_users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return None


def update_balance(chat_id, new_balance):
    """Обновление баланса пользователя"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('UPDATE casino_users SET balance = ? WHERE chat_id = ?', (new_balance, chat_id))
    connection.commit()
    connection.close()


def get_all_chat_ids():
    """Получение всех chat_id из базы данных"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT chat_id FROM casino_users')
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
