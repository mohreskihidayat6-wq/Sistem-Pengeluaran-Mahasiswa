import math
import random

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageTk

from controllers.auth_controller import AuthController
from views.splash_view import buat_logo_penuh

# ====== TEMA TAMPILAN (Glassmorphism & Konsisten dengan pengeluaran_view.py) ======
WARNA_KARTU = "#FFFFFF"         # Atau gunakan transisi warna jika ingin efek glass solid (mis: "#F4F2FC")
WARNA_INPUT = "#F7F6FB"
WARNA_BORDER = "#E3DFF2"
WARNA_GARIS = "#DDD8F0"
WARNA_AKSEN = "#6B5CB8"
WARNA_AKSEN_HOVER = "#5A4CA3"
WARNA_BANNER = "#E4DDFC"
WARNA_TOMBOL_TUTUP = "#F1EFFA"
WARNA_TEKS = "#1F1B2E"
WARNA_TEKS_REDUP = "#8E8AA3"

# warna latar marmer (turunan dari warna aksen)
MARMER_ATAS = "#8272D2"
MARMER_BAWAH = "#4F4195"
MARMER_PITA = (62, 48, 132)

LEBAR_JENDELA = 960
TINGGI_JENDELA = 700
LEBAR_FIELD = 350
RADIUS_KARTU = 24
POSISI_VERTIKAL = 0.57


# ----------------------------------------------------------------------
# Gambar (digambar dengan Pillow)
# ----------------------------------------------------------------------
def buat_latar_marmer(lebar, tinggi, logo=None, skala=1.0):
    """Latar ungu bermotif marmer (pita berkelok) + logo di bagian atas."""
    k = 4
    w, h = max(2, lebar // k), max(2, tinggi // k)
    acak = random.Random(21)

    def derau(nw, nh):
        kecil = Image.new("L", (nw, nh))
        kecil.putdata([acak.randint(0, 255) for _ in range(nw * nh)])
        return kecil.resize((w, h), Image.BICUBIC)

    medan = Image.blend(derau(5, 4), derau(9, 7), 0.45)
    medan = Image.blend(medan, derau(17, 12), 0.25)
    medan = ImageOps.autocontrast(medan)

    # gelombang periodik di atas medan acak -> pita berkelok seperti marmer
    tabel = [int(127.5 + 127.5 * math.sin(i / 255 * math.pi * 2 * 5))
             for i in range(256)]
    pita = medan.point(tabel)
    garis = pita.point(lambda v: int(max(0, v - 135) / 120 * 255))
    garis = garis.filter(ImageFilter.GaussianBlur(1.3))
    lembah = pita.point(lambda v: int(max(0, 95 - v) / 95 * 255))
    lembah = lembah.filter(ImageFilter.GaussianBlur(1.3))

    dasar = ImageOps.colorize(
        Image.linear_gradient("L").resize((w, h)),
        black=MARMER_ATAS, white=MARMER_BAWAH
    ).convert("RGB")
    dasar.paste(Image.new("RGB", (w, h), MARMER_PITA), (0, 0),
                garis.point(lambda v: int(v * 0.40)))
    dasar.paste(Image.new("RGB", (w, h), (170, 155, 240)), (0, 0),
                lembah.point(lambda v: int(v * 0.16)))

    hasil = dasar.resize((lebar, tinggi), Image.BICUBIC)

    if logo is not None:
        lebar_logo = int(230 * skala)
        tinggi_logo = int(lebar_logo * logo.height / logo.width)
        batas = int(78 * skala)
        if tinggi_logo > batas:
            tinggi_logo = batas
            lebar_logo = int(tinggi_logo * logo.width / logo.height)
        kecil = logo.resize((lebar_logo, tinggi_logo), Image.LANCZOS)
        hasil.paste(kecil, ((lebar - lebar_logo) // 2, int(34 * skala)), kecil)

    return hasil


def buat_sudut_kartu(latar, x, y, r, pojok):
    """Potongan sudut kartu: efek transparan/glass menyatu dengan latar marmer di luarnya."""
    potong = latar.crop((x, y, x + r, y + r)).convert("RGBA")
    
    # Berikan efek transparan tipis (glass overlay) pada sudut dalam kartu
    lapisan_kaca = Image.new("RGBA", (r, r), (255, 255, 255, 220))
    
    ss = 4
    pusat = {
        "kiri_atas": (r, r), "kanan_atas": (0, r),
        "kiri_bawah": (r, 0), "kanan_bawah": (0, 0),
    }[pojok]
    cx, cy = pusat[0] * ss, pusat[1] * ss
    topeng = Image.new("L", (r * ss, r * ss), 0)
    ImageDraw.Draw(topeng).ellipse(
        (cx - r * ss, cy - r * ss, cx + r * ss, cy + r * ss), fill=255
    )
    topeng = topeng.resize((r, r), Image.LANCZOS)
    
    return Image.composite(lapisan_kaca, potong, topeng).convert("RGB")


def buat_ikon_mata(coret, warna=(142, 138, 163, 255), ukuran=64):
    ss = 4
    U = ukuran * ss
    img = Image.new("RGBA", (U, U), (0, 0, 0, 0))
    pena = ImageDraw.Draw(img)
    c = U / 2
    w = int(U * 0.075)
    pena.ellipse((c - U * 0.40, c - U * 0.25, c + U * 0.40, c + U * 0.25),
                 outline=warna, width=w)
    r = U * 0.12
    pena.ellipse((c - r, c - r, c + r, c + r), fill=warna)
    if coret:
        pena.line((c - U * 0.34, c + U * 0.34, c + U * 0.34, c - U * 0.34),
                  fill=warna, width=w)
    return img.resize((ukuran, ukuran), Image.LANCZOS)


def buat_tombol_tutup(ukuran, warna_bg):
    """Tombol bulat dengan ikon silang (✕)."""
    ss = 4
    U = ukuran * ss
    img = Image.new("RGBA", (U, U), (0, 0, 0, 0))
    pena = ImageDraw.Draw(img)
    pena.ellipse((0, 0, U - 1, U - 1), fill=warna_bg)
    ungu = (107, 92, 184, 255)
    a, b = U * 0.34, U * 0.66
    w = int(U * 0.065)
    pena.line((a, a, b, b), fill=ungu, width=w)
    pena.line((a, b, b, a), fill=ungu, width=w)
    for x, y in ((a, a), (b, b), (a, b), (b, a)):
        pena.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=ungu)
    return img.resize((ukuran, ukuran), Image.LANCZOS)


# ----------------------------------------------------------------------
# Jendela login / registrasi
# ----------------------------------------------------------------------
class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Masuk - Pengelolaan Pengeluaran Mahasiswa")
        self.skala = max(1.0, self.winfo_fpixels("1i") / 96.0)
        x = (self.winfo_screenwidth() - int(LEBAR_JENDELA * self.skala)) // 2
        y = (self.winfo_screenheight() - int(TINGGI_JENDELA * self.skala)) // 2
        self.geometry(f"{LEBAR_JENDELA}x{TINGGI_JENDELA}+{x}+{max(0, y)}")
        self.resizable(False, False)
        self.configure(fg_color=MARMER_BAWAH)

        self.controller = AuthController()
        self.user = None
        self.mode = "login"
        self.sandi_terlihat = False
        self.foto = []
        self.foto_sudut = []

        self.buat_tampilan()
        self.ganti_mode("login")

        self.bind("<Return>", lambda event: self.proses())

    def _foto(self, gambar):
        foto = ImageTk.PhotoImage(gambar, master=self)
        self.foto.append(foto)
        return foto

    # ------------------------------------------------------------------
    def buat_tampilan(self):
        s = self.skala
        self.update_idletasks()
        self.lebar_px = max(self.winfo_width(), int(LEBAR_JENDELA * s))
        self.tinggi_px = max(self.winfo_height(), int(TINGGI_JENDELA * s))

        self.latar_pil = buat_latar_marmer(
            self.lebar_px, self.tinggi_px, buat_logo_penuh("putih"), s
        )
        tk.Label(
            self, image=self._foto(self.latar_pil), bd=0, highlightthickness=0
        ).place(x=0, y=0)

        # ikon
        ukuran_mata = int(22 * s)
        self.ikon_mata_tutup = self._foto(buat_ikon_mata(False, ukuran=ukuran_mata))
        self.ikon_mata_buka = self._foto(buat_ikon_mata(True, ukuran=ukuran_mata))
        ukuran_tutup = int(38 * s)
        self.ikon_tutup = self._foto(
            buat_tombol_tutup(ukuran_tutup, (241, 239, 250, 255)))
        self.ikon_tutup_hover = self._foto(
            buat_tombol_tutup(ukuran_tutup, (228, 221, 252, 255)))
        self.label_mata = []

        # kartu dengan nuansa semi-transparan (Glassmorphism Effect)
        self.kartu = ctk.CTkFrame(
            self, fg_color=("#FFFFFF", "#FFFFFF"), corner_radius=0
        )

        # ---- kepala: judul + tombol tutup ----
        kepala = ctk.CTkFrame(self.kartu, fg_color="transparent")
        kepala.pack(fill="x", padx=25, pady=(22, 18))

        self.label_judul = ctk.CTkLabel(
            kepala, text="", font=("Segoe UI", 22, "bold"),
            text_color=WARNA_TEKS
        )
        self.label_judul.pack(side="left")

        tombol_tutup = tk.Label(
            kepala, image=self.ikon_tutup, bd=0, highlightthickness=0,
            bg=WARNA_KARTU, cursor="hand2"
        )
        tombol_tutup.pack(side="right")
        tombol_tutup.bind("<Button-1>", lambda event: self.tutup())
        tombol_tutup.bind(
            "<Enter>", lambda e: tombol_tutup.configure(image=self.ikon_tutup_hover))
        tombol_tutup.bind(
            "<Leave>", lambda e: tombol_tutup.configure(image=self.ikon_tutup))

        self._garis()

        # ---- isian ----
        badan = ctk.CTkFrame(self.kartu, fg_color="transparent")
        badan.pack(fill="x", padx=25, pady=(24, 0))

        self.blok_nama, self.input_nama = self._kolom(
            badan, 0, "Nama Lengkap"
        )
        self.blok_username, self.input_username = self._kolom(
            badan, 1, "Username"
        )
        self.blok_password, self.input_password = self._kolom(
            badan, 2, "Password", rahasia=True
        )
        self.blok_konfirmasi, self.input_konfirmasi = self._kolom(
            badan, 3, "Konfirmasi Password", rahasia=True
        )

        self.tombol_utama = ctk.CTkButton(
            self.kartu, text="", height=48, corner_radius=14,
            font=("Segoe UI", 15, "bold"), fg_color=WARNA_AKSEN,
            hover_color=WARNA_AKSEN_HOVER, text_color="#FFFFFF",
            command=self.proses
        )
        self.tombol_utama.pack(fill="x", padx=25, pady=(10, 26))

        self._garis()

        # ---- kaki: pindah mode ----
        self.label_pindah = ctk.CTkLabel(
            self.kartu, text="", font=("Segoe UI", 12, "bold"),
            text_color=WARNA_AKSEN, cursor="hand2"
        )
        self.label_pindah.pack(pady=20)
        self.label_pindah.bind("<Button-1>", lambda event: self.pindah_mode())

        # empat potongan sudut (dibuat terakhir agar berada di atas kartu)
        self.sudut = {
            nama: tk.Label(self, bd=0, highlightthickness=0, padx=0, pady=0)
            for nama in ("kiri_atas", "kanan_atas", "kiri_bawah", "kanan_bawah")
        }

    def _garis(self):
        ctk.CTkFrame(self.kartu, height=1, fg_color=WARNA_GARIS,
                     corner_radius=0).pack(fill="x")

    def _kolom(self, induk, baris, teks, rahasia=False):
        gaya = dict(
            height=46, corner_radius=12, fg_color=WARNA_INPUT,
            border_color=WARNA_BORDER, border_width=1,
            text_color=WARNA_TEKS, placeholder_text_color=WARNA_TEKS_REDUP,
            font=("Segoe UI", 13)
        )

        if not rahasia:
            entry = ctk.CTkEntry(
                induk, width=LEBAR_FIELD, placeholder_text=teks, **gaya
            )
            entry.grid(row=baris, column=0, pady=(0, 12))
            return entry, entry

        pembungkus = ctk.CTkFrame(
            induk, width=LEBAR_FIELD, height=46, corner_radius=12,
            fg_color=WARNA_INPUT, border_color=WARNA_BORDER, border_width=1
        )
        pembungkus.grid(row=baris, column=0, pady=(0, 12))
        pembungkus.pack_propagate(False)

        mata = tk.Label(
            pembungkus, image=self.ikon_mata_tutup, bd=0,
            highlightthickness=0, bg=WARNA_INPUT, cursor="hand2"
        )
        mata.pack(side="right", padx=(0, 14))
        mata.bind("<Button-1>", lambda event: self.toggle_password())
        self.label_mata.append(mata)

        entry = ctk.CTkEntry(
            pembungkus, height=40, border_width=0, fg_color="transparent",
            text_color=WARNA_TEKS, placeholder_text=teks,
            placeholder_text_color=WARNA_TEKS_REDUP,
            font=("Segoe UI", 13), show="•"
        )
        entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        return pembungkus, entry

    # ------------------------------------------------------------------
    def _susun_kartu(self):
        """Menempatkan kartu di tengah dan memasang sudut bulat bergaya glass."""
        self.update_idletasks()
        w = self.kartu.winfo_reqwidth()
        h = self.kartu.winfo_reqheight()
        x = (self.lebar_px - w) // 2
        y = int(self.tinggi_px * POSISI_VERTIKAL - h / 2)
        tk.Place.place_configure(self.kartu, x=x, y=y)

        r = int(round(RADIUS_KARTU * self.skala))
        letak = {
            "kiri_atas": (x, y),
            "kanan_atas": (x + w - r, y),
            "kiri_bawah": (x, y + h - r),
            "kanan_bawah": (x + w - r, y + h - r),
        }
        self.foto_sudut = []
        for nama, (px, py) in letak.items():
            foto = ImageTk.PhotoImage(
                buat_sudut_kartu(self.latar_pil, px, py, r, nama), master=self
            )
            self.foto_sudut.append(foto)
            label = self.sudut[nama]
            label.configure(image=foto)
            label.place(x=px, y=py)
            label.lift()

    def _kosongkan(self, entry):
        if getattr(entry, "_placeholder_text_active", False):
            return
        entry.delete(0, "end")
        sedang_fokus = self.focus_get() is getattr(entry, "_entry", None)
        aktifkan = getattr(entry, "_activate_placeholder", None)
        if aktifkan is not None and not sedang_fokus:
            aktifkan()

    def toggle_password(self):
        self.sandi_terlihat = not self.sandi_terlihat
        tampilan = "" if self.sandi_terlihat else "•"
        for entry in (self.input_password, self.input_konfirmasi):
            entry.configure(show=tampilan)
        ikon = (self.ikon_mata_buka if self.sandi_terlihat
                else self.ikon_mata_tutup)
        for label in self.label_mata:
            label.configure(image=ikon)

    def tutup(self):
        self.user = None
        self.destroy()

    def ganti_mode(self, mode):
        self.mode = mode

        self._kosongkan(self.input_password)
        self._kosongkan(self.input_konfirmasi)

        if mode == "login":
            self.label_judul.configure(text="Masuk")
            self.blok_nama.grid_remove()
            self.blok_konfirmasi.grid_remove()
            self.tombol_utama.configure(text="Masuk")
            self.label_pindah.configure(text="Belum punya akun? Daftar")
            self.input_username.focus()
        else:
            self.label_judul.configure(text="Buat Akun")
            self.blok_nama.grid()
            self.blok_konfirmasi.grid()
            self.tombol_utama.configure(text="Daftar")
            self.label_pindah.configure(text="Sudah punya akun? Masuk")
            self.input_nama.focus()

        self._susun_kartu()

    def pindah_mode(self):
        self.ganti_mode("registrasi" if self.mode == "login" else "login")

    def proses(self):
        if self.mode == "login":
            self.proses_login()
        else:
            self.proses_registrasi()

    def proses_login(self):
        berhasil, pesan, user = self.controller.login(
            self.input_username.get(), self.input_password.get()
        )

        if berhasil:
            self.user = user
            self.destroy()
        else:
            messagebox.showwarning("Peringatan", pesan)

    def proses_registrasi(self):
        berhasil, pesan = self.controller.registrasi(
            self.input_nama.get(),
            self.input_username.get(),
            self.input_password.get(),
            self.input_konfirmasi.get()
        )

        if berhasil:
            messagebox.showinfo("Berhasil", pesan)
            username = self.input_username.get().strip()
            self._kosongkan(self.input_nama)
            self.ganti_mode("login")
            self._kosongkan(self.input_username)
            self.input_username.insert(0, username)
            self.input_password.focus()
        else:
            messagebox.showwarning("Peringatan", pesan)


def tampilkan_login():
    """Menampilkan jendela login. Mengembalikan data user, atau None jika ditutup."""
    login = LoginView()
    login.mainloop()
    return login.user