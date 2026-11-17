from config.database import get_connection


def get_user_by_username(username):
    connection = get_connection()

    if connection is None:
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT id_user, username, nama_lengkap, password
            FROM users
            WHERE username = %s
        """

        cursor.execute(query, (username,))
        return cursor.fetchone()

    except Exception as e:
        print("Gagal mengambil data user:", e)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def tambah_user(username, nama_lengkap, password_hash):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO users (username, nama_lengkap, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (username, nama_lengkap, password_hash))
        connection.commit()
        return True

    except Exception as e:
        print("Gagal menambah user:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()