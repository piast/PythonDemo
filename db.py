import sqlite3

import settings


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
    """
    def inner(*args, **kwargs):
        with sqlite3.connect(settings.DATABASE_NAME) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ :param conn: подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS audio')
        c.execute('DROP TABLE IF EXISTS photo')

    # audio type:
    c.execute('''
        CREATE TABLE IF NOT EXISTS audio (
            id                          INTEGER PRIMARY KEY,
            user_id                     INTEGER NOT NULL,
            file_id                     TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS photo (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            file_id     TEXT
        )
    ''')

    conn.commit()


@ensure_connection
def add_audio(conn, user_id: int, file_id: str):
    c = conn.cursor()
    c.execute('INSERT INTO audio (user_id, file_id) VALUES (?, ?)', (user_id, file_id))
    conn.commit()


@ensure_connection
def get_last_audio_num_by_user_id(conn, user_id: int):
    c = conn.cursor()
    c.execute('SELECT id FROM audio WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id, ))
    res = c.fetchone()
    return res[0] if res else 0


@ensure_connection
def get_list_audio_by_user_id(conn, user_id: int, limit: int = 10):
    c = conn.cursor()
    c.execute('SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()


@ensure_connection
def add_photo(conn, user_id: int, file_id: str):
    c = conn.cursor()
    c.execute('INSERT INTO photo (user_id, file_id) VALUES (?, ?)', (user_id, file_id))
    conn.commit()
