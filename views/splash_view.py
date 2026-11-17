import base64
import io
import random
import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, ImageTk

from views.logo_data import LOGO_IKON, LOGO_PENUH_PUTIH, LOGO_PENUH_BIRU

ctk.set_appearance_mode("dark")

WARNA_AKSEN = "#A5B4FC"
WARNA_JALUR = "#3E3C93"
WARNA_TEKS = "#FFFFFF"
WARNA_TEKS_REDUP = "#D6D9FF"

ALPHA_AKHIR = 0.97          # sedikit tembus pandang (1.0 = tidak tembus)

NAMA_APLIKASI = "Pengelolaan Pengeluaran Mahasiswa"

# lebar logo (satuan logis) saat animasi membesar
LEBAR_LOGO_AWAL = 380
LEBAR_LOGO_AKHIR = 560


def _muat_png(data_base64):
    return Image.open(io.BytesIO(base64.b64decode(data_base64))).convert("RGBA")


def buat_logo(ukuran=512):
    """Ikon SmartSaku (persegi, latar transparan)."""
    return _muat_png(LOGO_IKON).resize((ukuran, ukuran), Image.LANCZOS)


def buat_logo_penuh(warna="biru"):
    """Logo lengkap (ikon + tulisan SmartSaku) dengan latar transparan.

    warna="biru"  -> untuk latar terang
    warna="putih" -> untuk latar gelap / gradasi
    """
    return _muat_png(LOGO_PENUH_PUTIH if warna == "putih" else LOGO_PENUH_BIRU)


def gambar_logo_ctk(lebar, warna="biru"):
    """CTkImage logo lengkap dengan lebar tertentu (tinggi mengikuti rasio)."""
    logo = buat_logo_penuh(warna)
    tinggi = int(lebar * logo.height / logo.width)
    return ctk.CTkImage(light_image=logo, dark_image=logo,
                        size=(lebar, tinggi))


def buat_latar_kaca(lebar, tinggi):
    """Latar kaca buram (glassmorphism) seukuran layar.

    Dibuat dalam resolusi kecil lalu diperbesar: gradasinya halus, jadi
    hasilnya sama tetapi jauh lebih cepat.
    """
    k = 4
    W, H = max(1, lebar // k), max(1, tinggi // k)

    dasar = Image.new("RGBA", (W, H), (28, 24, 82, 255))
    acak = random.Random(5)
    warna = [
        (99, 102, 241), (168, 85, 247), (56, 189, 248),
        (236, 72, 153), (129, 140, 248), (34, 211, 238)
    ]
    blob = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pena = ImageDraw.Draw(blob)
    for i in range(8):
        r = acak.uniform(0.18, 0.34) * W
        cx = acak.uniform(0, W)
        cy = acak.uniform(0, H)
        pena.ellipse((cx - r, cy - r, cx + r, cy + r),
                     fill=warna[i % len(warna)] + (170,))
    blob = blob.filter(ImageFilter.GaussianBlur(W * 0.10))
    dasar = Image.alpha_composite(dasar, blob)

    # lapisan putih tipis (efek kaca)
    putih = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    dasar.paste(putih, (0, 0), Image.new("L", (W, H), 28))

    # kilau dari atas
    kilau = ImageOps.invert(Image.linear_gradient("L").resize((W, H)))
    kilau = kilau.point(lambda v: int(v * 0.25))
    dasar.paste(putih, (0, 0), kilau)

    return dasar.convert("RGB").resize((lebar, tinggi), Image.BICUBIC)


class SplashView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.skala = max(1.0, self.winfo_fpixels("1i") / 96.0)
        s = self.skala

        # Ukuran layar dalam piksel fisik. winfo_screenwidth() bisa
        # mengembalikan ukuran "logis" (lebih kecil) pada layar ber-scaling
        # 125%/150%, sehingga splash tidak memenuhi layar.
        lebar_layar, tinggi_layar = self._ukuran_layar()

        self.overrideredirect(True)
        self.attributes("-alpha", 0.0)
        self.attributes("-topmost", True)
        self.configure(fg_color="#1C1852")
        # tk.Tk.geometry dipanggil langsung agar CTk tidak menskalakan lagi
        tk.Tk.geometry(self, f"{lebar_layar}x{tinggi_layar}+0+0")
        self.update_idletasks()

        self.W = max(self.winfo_width(), lebar_layar)
        self.H = max(self.winfo_height(), tinggi_layar)

        self.logo_asli = buat_logo_penuh("putih")
        self.foto_logo = None

        self.kanvas = tk.Canvas(
            self, width=self.W, height=self.H, bd=0, highlightthickness=0,
            bg="#1C1852"
        )
        self.kanvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.foto_latar = ImageTk.PhotoImage(
            buat_latar_kaca(self.W, self.H), master=self
        )
        self.kanvas.create_image(0, 0, image=self.foto_latar, anchor="nw")

        cx, cy = self.W / 2, self.H / 2
        self.id_logo = self.kanvas.create_image(
            cx, cy - 40 * s, anchor="center"
        )
        self._set_logo(LEBAR_LOGO_AWAL)

        # progress bar (jalur + isian berujung bulat)
        self.bar_x0 = cx - 180 * s
        self.bar_x1 = cx + 180 * s
        self.bar_y = cy + 150 * s
        tebal = 6 * s
        self.kanvas.create_line(
            self.bar_x0, self.bar_y, self.bar_x1, self.bar_y,
            width=tebal, fill=WARNA_JALUR, capstyle="round"
        )
        self.id_isi = self.kanvas.create_line(
            self.bar_x0, self.bar_y, self.bar_x0, self.bar_y,
            width=tebal, fill=WARNA_AKSEN, capstyle="round"
        )
        self.id_status = self.kanvas.create_text(
            cx, cy + 180 * s, text="", fill=WARNA_TEKS_REDUP,
            font=("Segoe UI", 11)
        )

        self.after(50, self._fade_masuk)

    def _ukuran_layar(self):
        try:
            import ctypes
            user32 = ctypes.windll.user32
            lebar, tinggi = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            if lebar > 0 and tinggi > 0:
                return lebar, tinggi
        except (AttributeError, OSError):
            pass  # bukan Windows
        return self.winfo_screenwidth(), self.winfo_screenheight()

    def _set_logo(self, ukuran):
        px = max(1, int(ukuran * self.skala))
        py = max(1, int(px * self.logo_asli.height / self.logo_asli.width))
        gambar = self.logo_asli.resize((px, py), Image.LANCZOS)
        self.foto_logo = ImageTk.PhotoImage(gambar, master=self)
        self.kanvas.itemconfigure(self.id_logo, image=self.foto_logo)

    def _set_bar(self, nilai):
        x = self.bar_x0 + (self.bar_x1 - self.bar_x0) * nilai
        self.kanvas.coords(self.id_isi, self.bar_x0, self.bar_y, x, self.bar_y)

    # 1) layar muncul perlahan
    def _fade_masuk(self, langkah=0):
        self.attributes("-alpha", ALPHA_AKHIR * min(1.0, langkah / 15))
        if langkah < 15:
            self.after(25, self._fade_masuk, langkah + 1)
        else:
            self._logo_membesar()

    # 2) logo membesar dengan efek melambat
    def _logo_membesar(self, langkah=0):
        total = 20
        t = langkah / total
        ease = 1 - (1 - t) ** 3
        self._set_logo(int(LEBAR_LOGO_AWAL +
                           (LEBAR_LOGO_AKHIR - LEBAR_LOGO_AWAL) * ease))
        if langkah < total:
            self.after(20, self._logo_membesar, langkah + 1)
        else:
            self.after(150, self._muat)

    # 3) progress bar terisi
    def _muat(self, langkah=0):
        total = 40
        pesan = (
            (0, "Menyiapkan aplikasi..."),
            (14, "Menghubungkan database..."),
            (28, "Memuat data..."),
        )
        for batas, teks in pesan:
            if langkah >= batas:
                self.kanvas.itemconfigure(self.id_status, text=teks)
        self._set_bar(langkah / total)
        if langkah < total:
            self.after(35, self._muat, langkah + 1)
        else:
            self.after(250, self._fade_keluar)

    # 4) layar menghilang lalu ditutup
    def _fade_keluar(self, langkah=0):
        self.attributes("-alpha", max(0.0, ALPHA_AKHIR * (1 - langkah / 12)))
        if langkah < 12:
            self.after(25, self._fade_keluar, langkah + 1)
        else:
            self.destroy()


def tampilkan_splash():
    splash = SplashView()
    splash.mainloop()