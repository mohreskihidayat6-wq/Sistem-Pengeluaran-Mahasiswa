from models.pengeluaran_model import (
    get_all_pengeluaran,
    tambah_pengeluaran,
    ubah_pengeluaran,
    hapus_pengeluaran
)


class PengeluaranController:

    def __init__(self, id_user=None):
        self.id_user = id_user

    def tampilkan_pengeluaran(self):
        return get_all_pengeluaran(self.id_user)

    def tambah(
        self,
        id_kategori,
        tanggal,
        nominal,
        deskripsi
    ):
        return tambah_pengeluaran(
            self.id_user,
            id_kategori,
            tanggal,
            nominal,
            deskripsi
        )

    def ubah(
        self,
        id_pengeluaran,
        id_kategori,
        tanggal,
        nominal,
        deskripsi
    ):
        return ubah_pengeluaran(
            self.id_user,
            id_pengeluaran,
            id_kategori,
            tanggal,
            nominal,
            deskripsi
        )

    def hapus(self, id_pengeluaran):
        return hapus_pengeluaran(self.id_user, id_pengeluaran)