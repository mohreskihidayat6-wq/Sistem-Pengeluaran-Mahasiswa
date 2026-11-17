import hashlib
import hmac
import os
import re

from models.user_model import get_user_by_username, tambah_user


class AuthController:
    JUMLAH_ITERASI = 120000

    def hash_password(self, password):
        salt = os.urandom(16)
        hasil = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.JUMLAH_ITERASI
        )
        return f"{salt.hex()}${hasil.hex()}"

    def cek_password(self, password, tersimpan):
        try:
            salt_hex, hash_hex = tersimpan.split("$")
            salt = bytes.fromhex(salt_hex)
            hasil = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, self.JUMLAH_ITERASI
            )
            return hmac.compare_digest(hasil.hex(), hash_hex)
        except (ValueError, AttributeError):
            return False

    def login(self, username, password):
        """Mengembalikan (berhasil, pesan, data_user)."""
        username = username.strip()

        if not username or not password:
            return False, "Username dan password wajib diisi.", None

        user = get_user_by_username(username)

        if user is None or not self.cek_password(password, user["password"]):
            return False, "Username atau password salah.", None

        return True, "Login berhasil.", {
            "id_user": user["id_user"],
            "username": user["username"],
            "nama_lengkap": user["nama_lengkap"],
        }

    def registrasi(self, nama_lengkap, username, password, konfirmasi):
        """Mengembalikan (berhasil, pesan)."""
        nama_lengkap = nama_lengkap.strip()
        username = username.strip()

        if not nama_lengkap or not username or not password:
            return False, "Semua kolom wajib diisi."

        if not re.fullmatch(r"[A-Za-z0-9_]{4,30}", username):
            return False, (
                "Username 4-30 karakter, hanya huruf, angka, dan underscore."
            )

        if len(password) < 6:
            return False, "Password minimal 6 karakter."

        if password != konfirmasi:
            return False, "Konfirmasi password tidak sama."

        if get_user_by_username(username) is not None:
            return False, "Username sudah dipakai, coba yang lain."

        if tambah_user(username, nama_lengkap, self.hash_password(password)):
            return True, "Akun berhasil dibuat. Silakan masuk."

        return False, "Registrasi gagal. Periksa koneksi database."