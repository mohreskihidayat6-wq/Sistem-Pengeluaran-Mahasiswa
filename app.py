import customtkinter as ctk

from views.splash_view import tampilkan_splash
from views.login_view import tampilkan_login
from views.pengeluaran_view import PengeluaranView


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # 1. Tampilkan animasi splash screen di awal
    try:
        tampilkan_splash()
    except Exception as e:
        print(f"Error pada splash screen: {e}")

    while True:
        # 2. Tampilkan form login dan tunggu hingga user berhasil masuk atau menutup jendela
        try:
            user = tampilkan_login()
        except Exception as e:
            print(f"Error pada halaman login: {e}")
            break

        # Jika user menutup jendela login (mengembalikan nilai None), hentikan program sepenuhnya
        if user is None:
            break

        # 3. Jalankan jendela utama aplikasi (Dashboard & Pengeluaran)
        try:
            app = PengeluaranView(user)
            app.mainloop()
        except Exception as e:
            print(f"Error pada jendela utama: {e}")
            break

        # 4. Ambil status apakah tombol logout yang ditekan
        is_logout = getattr(app, "keluar_akun", False)

        # Hancurkan sisa window aplikasi utama secara aman dari memori
        try:
            app.destroy()
        except Exception:
            pass

        # 5. Jika logout bernilai True, lanjut perulangan untuk menampilkan kembali halaman login
        if is_logout:
            continue
        else:
            break     # Jika jendela ditutup biasa (bukan tombol logout), keluar program