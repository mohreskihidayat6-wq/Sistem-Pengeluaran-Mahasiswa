from config.database import get_connection


def get_all_pengeluaran(id_user):
    connection = get_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                p.id_pengeluaran,
                u.nama_lengkap AS nama_user,
                k.nama_kategori,
                p.tanggal,
                p.nominal,
                p.deskripsi
            FROM pengeluaran p
            JOIN users u
                ON p.id_user = u.id_user
            JOIN kategori k
                ON p.id_kategori = k.id_kategori
            WHERE p.id_user = %s
            ORDER BY p.tanggal DESC
        """

        cursor.execute(query, (id_user,))
        return cursor.fetchall()

    except Exception as e:
        print("Gagal mengambil data pengeluaran:", e)
        return []

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def tambah_pengeluaran(
    id_user,
    id_kategori,
    tanggal,
    nominal,
    deskripsi
):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO pengeluaran
            (id_user, id_kategori, tanggal, nominal, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            id_user,
            id_kategori,
            tanggal,
            nominal,
            deskripsi
        )

        cursor.execute(query, values)
        connection.commit()

        return True

    except Exception as e:
        connection.rollback()
        print("Gagal menambahkan pengeluaran:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def ubah_pengeluaran(
    id_user,
    id_pengeluaran,
    id_kategori,
    tanggal,
    nominal,
    deskripsi
):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE pengeluaran
            SET id_kategori = %s,
                tanggal = %s,
                nominal = %s,
                deskripsi = %s
            WHERE id_pengeluaran = %s
              AND id_user = %s
        """

        values = (
            id_kategori,
            tanggal,
            nominal,
            deskripsi,
            id_pengeluaran,
            id_user
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount > 0

    except Exception as e:
        connection.rollback()
        print("Gagal mengubah pengeluaran:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def hapus_pengeluaran(id_user, id_pengeluaran):
    connection = get_connection()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            DELETE FROM pengeluaran
            WHERE id_pengeluaran = %s
              AND id_user = %s
        """

        cursor.execute(query, (id_pengeluaran, id_user))
        connection.commit()

        return cursor.rowcount > 0

    except Exception as e:
        connection.rollback()
        print("Gagal menghapus pengeluaran:", e)
        return False

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()