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

import sqlite3

DATABASE_PATH = "intellect.db"

def init_trivia_db():
    """
    Проверяет структуру таблицы 'players'. Если структура не соответствует требованиям,
    пересоздает таблицу с правильными столбцами.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # Получаем информацию о столбцах таблицы
    cursor.execute("PRAGMA table_info(players)")
    columns = [column[1] for column in cursor.fetchall()]  # Список имен столбцов

    # Если таблицы нет или отсутствуют критические столбцы, пересоздаем таблицу
    if 'chat_id' not in columns or 'name' not in columns or 'intelligence_points' not in columns:
        print("Пересоздание таблицы 'players' с корректной структурой...")

        # Переименовываем старую таблицу, если она существует
        cursor.execute("DROP TABLE IF EXISTS players")

        # Создаем новую таблицу с правильной структурой
        cursor.execute("""
            CREATE TABLE players (
                chat_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                intelligence_points INTEGER DEFAULT 0
            )
        """)

    connection.commit()
    connection.close()


def add_player_to_db(chat_id, name):
    """Добавление пользователя в базу данных, если он ещё не добавлен"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT chat_id FROM players WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()

        if not result:
            cursor.execute("INSERT INTO players (chat_id, name, intelligence_points) VALUES (?, ?, ?)",
                           (chat_id, name, 0))
            connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite error при добавлении пользователя: {e}")
    finally:
        connection.close()


def get_intelligence_points_by_chat_id(chat_id):
    """Получение текущих очков интеллекта пользователя по chat_id"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT intelligence_points FROM players WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            print(f"Пользователь с chat_id '{chat_id}' не найден в базе данных.")
            return None

    except sqlite3.Error as e:
        print(f"Ошибка при получении очков интеллекта: {e}")
        return None
    finally:
        connection.close()
def update_intelligence_points(chat_id, points):
    """
    Обновление очков интеллекта пользователя.
    Если пользователь не существует, ничего не произойдет.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE players 
            SET intelligence_points = intelligence_points + ? 
            WHERE chat_id = ?
        """, (points, chat_id))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении очков интеллекта: {e}")
    finally:
        connection.close()
