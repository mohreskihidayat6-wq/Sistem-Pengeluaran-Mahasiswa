import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
from datetime import date
import csv
import math
import random

from PIL import (Image, ImageChops, ImageColor, ImageDraw, ImageFilter,
                 ImageOps, ImageTk)

from models.kategori_model import get_all_kategori
from controllers.pengeluaran_controller import PengeluaranController
from views.splash_view import buat_logo


# ====== TEMA TAMPILAN (terang dengan aksen ungu) ======
WARNA_BG = "#FFFFFF"
WARNA_SIDEBAR = "#FAF9FF"
WARNA_KARTU = "#F7F6FB"
WARNA_BANNER = "#E4DDFC"
WARNA_BORDER = "#E3DFF2"
WARNA_AKSEN = "#6B5CB8"
WARNA_AKSEN_HOVER = "#5A4CA3"
WARNA_AKSEN_MUDA = "#D9D2F5"
WARNA_BAHAYA = "#E5484D"
WARNA_BAHAYA_HOVER = "#CF3A3F"
WARNA_NETRAL = "#8E8AA3"
WARNA_NETRAL_HOVER = "#78748E"
WARNA_TEKS = "#1F1B2E"
WARNA_TEKS_REDUP = "#8E8AA3"
WARNA_BARIS_A = "#FFFFFF"
WARNA_BARIS_B = "#F7F6FB"

FONT_JUDUL = ("Segoe UI", 22, "bold")
FONT_SAPA = ("Georgia", 30, "bold")
FONT_LABEL = ("Segoe UI", 12, "bold")
FONT_INPUT = ("Segoe UI", 13)
FONT_TOMBOL = ("Segoe UI", 13, "bold")
FONT_KECIL = ("Segoe UI", 11)

NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_BULAN = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

def bersihkan_nominal(teks):
    bersih = str(teks).replace("Rp", "").replace(".", "").replace(",", "").strip()
    return int(bersih) if bersih.isdigit() else 0


# ====== TOMBOL EFEK KACA (GLASS) ======
_CACHE_KACA = {}


def _topeng_ikon(nama, S):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)

    def p(v):
        return v * S

    def garis(titik, tebal, nilai=255):
        w = max(1, int(p(tebal)))
        for a, b in zip(titik[:-1], titik[1:]):
            d.line([(p(a[0]), p(a[1])), (p(b[0]), p(b[1]))],
                   fill=nilai, width=w)
        r = w / 2
        for x, y in titik:
            d.ellipse((p(x) - r, p(y) - r, p(x) + r, p(y) + r), fill=nilai)

    def busur(cx, cy, R, w, awal, akhir):
        w = int(w)
        d.arc((cx - R, cy - R, cx + R, cy + R),
              start=awal, end=akhir, fill=255, width=w)
        rc = R - w / 2
        for sudut in (awal, akhir):
            t = math.radians(sudut)
            x, y = cx + rc * math.cos(t), cy + rc * math.sin(t)
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=255)

    if nama == "tambah":
        garis([(.14, .5), (.86, .5)], .2)
        garis([(.5, .14), (.5, .86)], .2)

    elif nama == "pensil":
        B = int(S * 1.5)
        L = S * 1.38
        w = S * .30
        cx, atas = B / 2, (B - L) / 2
        k = Image.new("L", (B, B), 0)
        kd = ImageDraw.Draw(k)
        kd.rounded_rectangle(
            (cx - w / 2, atas, cx + w / 2, atas + S * .17),
            radius=S * .05, fill=255
        )
        kd.rectangle(
            (cx - w / 2, atas + S * .22, cx + w / 2, atas + L - S * .32),
            fill=255
        )
        kd.polygon([
            (cx - w / 2, atas + L - S * .27),
            (cx + w / 2, atas + L - S * .27),
            (cx, atas + L),
        ], fill=255)
        k = k.rotate(-45, resample=Image.BICUBIC)
        o = (B - S) // 2
        m = k.crop((o, o, o + S, o + S))

    elif nama == "sampah":
        d.rounded_rectangle(
            (p(.34), p(.04), p(.66), p(.24)), radius=p(.06), fill=255
        )
        d.rounded_rectangle(
            (p(.43), p(.12), p(.57), p(.24)), radius=p(.02), fill=0
        )
        d.rounded_rectangle(
            (p(.08), p(.2), p(.92), p(.32)), radius=p(.05), fill=255
        )
        d.rounded_rectangle(
            (p(.2), p(.38), p(.8), p(.96)), radius=p(.08), fill=255
        )
        for x in (.38, .5, .62):
            garis([(x, .5), (x, .82)], .07, 0)

    elif nama == "segarkan":
        R, w = S * .40, S * .14
        busur(S / 2, S / 2, R, w, 40, 320)
        rc = R - w / 2
        t = math.radians(320)
        px, py = S / 2 + rc * math.cos(t), S / 2 + rc * math.sin(t)
        tx, ty = -math.sin(t), math.cos(t)
        nx, ny = math.cos(t), math.sin(t)
        d.polygon([
            (px + tx * S * .24, py + ty * S * .24),
            (px + nx * S * .22 - tx * S * .04,
             py + ny * S * .22 - ty * S * .04),
            (px - nx * S * .22 - tx * S * .04,
             py - ny * S * .22 - ty * S * .04),
        ], fill=255)

    elif nama == "unduh":
        garis([(.5, .08), (.5, .52)], .17)
        d.polygon(
            [(p(.2), p(.46)), (p(.8), p(.46)), (p(.5), p(.78))], fill=255
        )
        garis([(.14, .74), (.14, .9), (.86, .9), (.86, .74)], .12)

    elif nama == "daya":
        busur(S / 2, S * .56, S * .38, S * .14, 310, 230)
        garis([(.5, .08), (.5, .5)], .14)

    elif nama == "kisi":
        for x, y in ((.1, .1), (.55, .1), (.1, .55), (.55, .55)):
            d.rounded_rectangle(
                (p(x), p(y), p(x + .35), p(y + .35)),
                radius=p(.08), fill=255
            )

    elif nama == "kalender":
        d.rounded_rectangle(
            (p(.1), p(.16), p(.9), p(.94)), radius=p(.12), fill=255
        )
        d.rounded_rectangle(
            (p(.18), p(.40), p(.82), p(.86)), radius=p(.05), fill=0
        )
        for x in (.28, .64):
            d.rounded_rectangle(
                (p(x), p(.04), p(x + .09), p(.3)), radius=p(.04), fill=255
            )
        for cx in (.3, .5, .7):
            for cy in (.52, .72):
                d.rounded_rectangle(
                    (p(cx - .06), p(cy - .06), p(cx + .06), p(cy + .06)),
                    radius=p(.02), fill=255
                )

    elif nama == "uang":
        d.ellipse((p(.08), p(.32), p(.92), p(.97)), fill=255)
        d.polygon(
            [(p(.34), p(.1)), (p(.66), p(.1)),
             (p(.76), p(.46)), (p(.24), p(.46))], fill=255
        )
        d.rounded_rectangle(
            (p(.27), p(.02), p(.73), p(.16)), radius=p(.05), fill=255
        )
        garis([(.26, .42), (.74, .42)], .06, 0)
        w = max(1, int(S * .06))
        d.arc((p(.37), p(.52), p(.63), p(.72)), 90, 330, fill=0, width=w)
        d.arc((p(.37), p(.70), p(.63), p(.90)), 270, 150, fill=0, width=w)
        d.rectangle((p(.485), p(.49), p(.515), p(.93)), fill=0)

    elif nama == "struk":
        d.polygon([
            (p(.2), p(.04)), (p(.8), p(.04)), (p(.8), p(.96)),
            (p(.7), p(.88)), (p(.6), p(.96)), (p(.5), p(.88)),
            (p(.4), p(.96)), (p(.3), p(.88)), (p(.2), p(.96)),
        ], fill=255)
        for y in (.24, .42, .60):
            garis([(.34, y), (.66, y)], .07, 0)

    elif nama == "label":
        d.polygon([
            (p(.06), p(.06)), (p(.52), p(.06)), (p(.94), p(.48)),
            (p(.48), p(.94)), (p(.06), p(.52)),
        ], fill=255)
        d.ellipse((p(.2), p(.2), p(.38), p(.38)), fill=0)

    elif nama == "catatan":
        d.rounded_rectangle(
            (p(.16), p(.05), p(.84), p(.95)), radius=p(.1), fill=255
        )
        garis([(.32, .3), (.68, .3)], .08, 0)
        garis([(.32, .5), (.68, .5)], .08, 0)
        garis([(.32, .7), (.52, .7)], .08, 0)

    return m


def _campur(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def buat_gambar_kaca(lebar, tinggi, warna, mode="tebal", keadaan="normal",
                     radius=10, ikon=None, ikon_x=0, ikon_ukuran=18,
                     ikon_warna="#FFFFFF"):
    kunci = (lebar, tinggi, warna, mode, keadaan, radius,
             ikon, ikon_x, ikon_ukuran, ikon_warna)
    if kunci in _CACHE_KACA:
        return _CACHE_KACA[kunci]

    skala = 3
    W, H = lebar * skala, tinggi * skala
    r = min(radius * skala, H // 2)
    rgb = ImageColor.getrgb(warna)
    putih = (255, 255, 255)

    if mode == "tebal":
        atas = _campur(rgb, putih, 0.30)
        bawah = rgb
        a_atas, a_bawah = 225, 245
    else:
        atas = _campur(rgb, putih, 0.60)
        bawah = _campur(rgb, putih, 0.30)
        a_atas, a_bawah = 120, 170

    if keadaan == "hover":
        atas = _campur(atas, putih, 0.15)
        bawah = _campur(bawah, putih, 0.10)
        a_atas, a_bawah = min(255, a_atas + 30), min(255, a_bawah + 30)
    elif keadaan == "tekan":
        atas = _campur(atas, (0, 0, 0), 0.15)
        bawah = _campur(bawah, (0, 0, 0), 0.15)

    grad = Image.linear_gradient("L").resize((W, H))
    warna_img = Image.composite(
        Image.new("RGB", (W, H), bawah), Image.new("RGB", (W, H), atas), grad
    )
    alpha = grad.point(lambda v: int(a_atas + (a_bawah - a_atas) * v / 255))
    dasar = warna_img.convert("RGBA")
    dasar.putalpha(alpha)

    m = 2 * skala
    tinggi_kilau = int(H * 0.55)
    kilau_alpha = ImageOps.invert(
        Image.linear_gradient("L").resize((W, tinggi_kilau))
    ).point(lambda v: int(v * 0.42))
    kilau_penuh = Image.new("L", (W, H), 0)
    kilau_penuh.paste(kilau_alpha, (0, 0))
    topeng_kilau = Image.new("L", (W, H), 0)
    ImageDraw.Draw(topeng_kilau).rounded_rectangle(
        (m, m, W - m - 1, H - m - 1), max(1, r - m), fill=255
    )
    kilau = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    kilau.putalpha(ImageChops.multiply(kilau_penuh, topeng_kilau))

    tepi = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pena = ImageDraw.Draw(tepi)
    warna_tepi = _campur(rgb, (0, 0, 0), 0.20)
    pena.rounded_rectangle(
        (0, 0, W - 1, H - 1), r, outline=warna_tepi + (110,), width=skala
    )
    pena.rounded_rectangle(
        (skala, skala, W - skala - 1, H - skala - 1), max(1, r - skala),
        outline=(255, 255, 255, 190), width=skala
    )

    hasil = Image.alpha_composite(dasar, kilau)

    if ikon:
        S = ikon_ukuran * skala
        x0 = int(round(ikon_x * skala))
        y0 = (H - S) // 2
        topeng_ikon = _topeng_ikon(ikon, S)
        rgb_ikon = ImageColor.getrgb(ikon_warna)
        isi = Image.composite(
            Image.new("RGB", (S, S), _campur(rgb_ikon, (0, 0, 0), 0.12)),
            Image.new("RGB", (S, S), _campur(rgb_ikon, putih, 0.08)),
            Image.linear_gradient("L").resize((S, S))
        ).convert("RGBA")
        isi.putalpha(topeng_ikon)

        if mode == "tebal":
            bayangan = Image.new("L", (W, H), 0)
            bayangan.paste(topeng_ikon, (x0, y0 + skala))
            bayangan = bayangan.filter(
                ImageFilter.GaussianBlur(skala)
            ).point(lambda v: int(v * 0.5))
            lapisan_b = Image.new("RGBA", (W, H), (20, 10, 60, 0))
            lapisan_b.putalpha(bayangan)
            hasil = Image.alpha_composite(hasil, lapisan_b)

        lapisan_i = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lapisan_i.paste(isi, (x0, y0))
        hasil = Image.alpha_composite(hasil, lapisan_i)

    hasil = Image.alpha_composite(hasil, tepi)

    topeng = Image.new("L", (W, H), 0)
    ImageDraw.Draw(topeng).rounded_rectangle(
        (0, 0, W - 1, H - 1), r, fill=255
    )
    hasil.putalpha(ImageChops.multiply(hasil.getchannel("A"), topeng))

    hasil = hasil.resize((lebar * 2, tinggi * 2), Image.LANCZOS)
    gambar = ctk.CTkImage(
        light_image=hasil, dark_image=hasil, size=(lebar, tinggi)
    )
    _CACHE_KACA[kunci] = gambar
    return gambar


class TombolKaca(ctk.CTkLabel):
    def __init__(self, induk, teks, lebar, tinggi, warna, perintah=None,
                 mode="tebal", warna_teks="#FFFFFF", font=FONT_TOMBOL,
                 radius=10, ikon=None, ikon_ukuran=18, ikon_warna=None):
        self._lebar = lebar
        self._tinggi = tinggi
        self._warna = warna
        self._mode = mode
        self._radius = radius
        self._perintah = perintah
        self._di_atas = False
        self._ikon = ikon
        self._ikon_ukuran = ikon_ukuran
        self._ikon_warna = ikon_warna or warna_teks
        self._ikon_x = 0

        font_ctk = ctk.CTkFont(
            family=font[0], size=font[1],
            weight=font[2] if len(font) > 2 else "normal"
        )
        teks_tampil = teks
        if ikon and teks:
            lebar_teks = font_ctk.measure(teks)
            lebar_spasi = max(1, font_ctk.measure(" "))
            n = max(1, round((ikon_ukuran + 8) / lebar_spasi))
            geser = n * lebar_spasi
            teks_tampil = " " * n + teks
            self._ikon_x = (lebar - (geser + lebar_teks)) / 2
        elif ikon:
            self._ikon_x = (lebar - ikon_ukuran) / 2

        super().__init__(
            induk, text=teks_tampil, width=lebar, height=tinggi,
            image=self._gambar("normal"), compound="center",
            text_color=warna_teks, font=font_ctk,
            fg_color="transparent", corner_radius=0
        )

        for bagian in (self._label, self._canvas):
            try:
                bagian.configure(cursor="hand2")
            except tk.TclError:
                pass

        self.bind("<Enter>", self._masuk)
        self.bind("<Leave>", self._keluar)
        self.bind("<ButtonPress-1>", self._tekan)
        self.bind("<ButtonRelease-1>", self._lepas)

    def _gambar(self, keadaan):
        return buat_gambar_kaca(
            self._lebar, self._tinggi, self._warna,
            self._mode, keadaan, self._radius,
            self._ikon, self._ikon_x, self._ikon_ukuran, self._ikon_warna
        )

    def _masuk(self, event=None):
        self._di_atas = True
        self.configure(image=self._gambar("hover"))

    def _keluar(self, event=None):
        self._di_atas = False
        self.configure(image=self._gambar("normal"))

    def _tekan(self, event=None):
        self.configure(image=self._gambar("tekan"))

    def _lepas(self, event):
        w = self.winfo_containing(event.x_root, event.y_root)
        di_dalam = False
        while w is not None:
            if w is self:
                di_dalam = True
                break
            w = w.master
        self.configure(image=self._gambar("hover" if di_dalam else "normal"))
        if di_dalam and self._perintah:
            self._perintah()

    def atur_gaya(self, mode=None, warna=None, warna_teks=None,
                  ikon_warna=None):
        if mode is not None:
            self._mode = mode
        if warna is not None:
            self._warna = warna
        if ikon_warna is not None:
            self._ikon_warna = ikon_warna
        if warna_teks is not None:
            self.configure(text_color=warna_teks)
        self.configure(image=self._gambar("normal"))


class KomboRapi(ctk.CTkComboBox):
    def _draw(self, no_color_updates=False):
        super()._draw(no_color_updates)
        try:
            kanvas = self._canvas
            kanvas.delete("dropdown_arrow")
            kanvas.delete("chevron")
            h = self._apply_widget_scaling(self._current_height)
            w = self._apply_widget_scaling(self._current_width)
            cx, cy = w - h / 2, h / 2
            u = h / 8
            kanvas.create_line(
                cx - 1.6 * u, cy - 0.7 * u,
                cx, cy + 0.9 * u,
                cx + 1.6 * u, cy - 0.7 * u,
                fill="#FFFFFF", width=max(2, int(h / 16)),
                capstyle="round", joinstyle="round", tags="chevron"
            )
        except Exception:
            pass


class PengeluaranView(ctk.CTk):
    def __init__(self, user=None):
        super().__init__()

        self.title("Aplikasi Pengelolaan Pengeluaran Mahasiswa")
        self.geometry("1280x780")
        self.minsize(1100, 700)
        self.configure(fg_color=WARNA_BG)

        self.user = user
        self.controller = PengeluaranController(
            user["id_user"] if user else None
        )
        self.data_kategori = []
        self.id_terpilih = None
        self.keluar_akun = False
        self.data_pengeluaran = []

        self.buat_tampilan()
        self.muat_pilihan()
        self.tampilkan_data()
        self.tampilkan_halaman("dashboard")

    def destroy(self):
        """Membersihkan cache tombol kaca saat jendela dihancurkan agar tidak konflik pyimage saat login ulang."""
        global _CACHE_KACA
        _CACHE_KACA.clear()
        super().destroy()

    def _gaya_tabel(self):
        gaya = ttk.Style(self)
        gaya.theme_use("clam")

        gaya.configure(
            "Treeview",
            background=WARNA_BARIS_A,
            fieldbackground=WARNA_BARIS_A,
            foreground=WARNA_TEKS,
            rowheight=36,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 12)
        )
        gaya.configure(
            "Treeview.Heading",
            background="#EDE9FB",
            foreground=WARNA_TEKS,
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            borderwidth=0,
            padding=(10, 10)
        )
        gaya.map(
            "Treeview",
            background=[("selected", WARNA_AKSEN)],
            foreground=[("selected", "#FFFFFF")]
        )
        gaya.map(
            "Treeview.Heading",
            background=[("active", WARNA_AKSEN_MUDA)]
        )
        gaya.layout(
            "Treeview", [("Treeview.treearea", {"sticky": "nswe"})]
        )

        gaya.configure(
            "Vertical.TScrollbar",
            background="#CFC9E6",
            troughcolor=WARNA_KARTU,
            bordercolor=WARNA_KARTU,
            arrowcolor=WARNA_TEKS_REDUP,
            lightcolor="#CFC9E6",
            darkcolor="#CFC9E6",
            relief="flat",
            gripcount=0
        )
        gaya.map(
            "Vertical.TScrollbar",
            background=[("active", WARNA_NETRAL)]
        )

    def _gaya_entry(self):
        return dict(
            height=40,
            corner_radius=8,
            fg_color="#FFFFFF",
            border_color=WARNA_BORDER,
            border_width=1,
            text_color=WARNA_TEKS,
            placeholder_text_color=WARNA_TEKS_REDUP,
            font=FONT_INPUT
        )

    def _gaya_combo(self):
        return dict(
            height=40,
            corner_radius=8,
            fg_color="#FFFFFF",
            border_color=WARNA_BORDER,
            border_width=1,
            button_color=WARNA_AKSEN,
            button_hover_color=WARNA_AKSEN_HOVER,
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color=WARNA_AKSEN_MUDA,
            dropdown_text_color=WARNA_TEKS,
            text_color=WARNA_TEKS,
            font=FONT_INPUT,
            dropdown_font=FONT_INPUT
        )

    def _label_form(self, parent, teks, baris, kolom):
        ctk.CTkLabel(
            parent,
            text=teks,
            font=FONT_LABEL,
            text_color=WARNA_TEKS_REDUP
        ).grid(row=baris, column=kolom, padx=(20, 10), pady=10, sticky="w")

    def buat_tampilan(self):
        self._gaya_tabel()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.buat_sidebar()

        utama = ctk.CTkFrame(self, fg_color=WARNA_BG, corner_radius=0)
        utama.grid(row=0, column=1, sticky="nsew")

        self.buat_header(utama)

        self.area = ctk.CTkFrame(utama, fg_color="transparent")
        self.area.pack(fill="both", expand=True, padx=35, pady=(10, 25))

        self.buat_halaman_dashboard()
        self.buat_halaman_pengeluaran()

    def buat_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, width=240, fg_color=WARNA_SIDEBAR, corner_radius=0
        )
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False)

        logo = buat_logo(128)
        self.gambar_logo = ctk.CTkImage(
            light_image=logo, dark_image=logo, size=(42, 42)
        )

        baris_logo = ctk.CTkFrame(sidebar, fg_color="transparent")
        baris_logo.pack(fill="x", padx=25, pady=(30, 25))
        ctk.CTkLabel(baris_logo, text="", image=self.gambar_logo).pack(
            side="left"
        )
        ctk.CTkLabel(
            baris_logo, text="Pengeluaran\nMahasiswa",
            font=("Segoe UI", 14, "bold"), text_color=WARNA_TEKS,
            justify="left"
        ).pack(side="left", padx=10)

        kartu_tambah = ctk.CTkFrame(
            sidebar, fg_color="#F1EFFA", corner_radius=14
        )
        kartu_tambah.pack(fill="x", padx=20, pady=(0, 25))
        ctk.CTkLabel(
            kartu_tambah, text="Tambah\nPengeluaran",
            font=("Segoe UI", 13, "bold"), text_color=WARNA_TEKS,
            justify="left"
        ).pack(side="left", padx=(15, 5), pady=14)
        TombolKaca(
            kartu_tambah, "", 42, 42, WARNA_AKSEN,
            perintah=self.buka_form_baru,
            radius=21, ikon="tambah", ikon_ukuran=20
        ).pack(side="right", padx=15)

        self.tombol_nav = {}
        menu = (
            ("dashboard", "Dashboard", "kisi"),
            ("pengeluaran", "Pengeluaran", "catatan"),
        )
        for kunci, teks, ikon in menu:
            tombol = TombolKaca(
                sidebar, teks, 200, 44, WARNA_AKSEN,
                perintah=lambda k=kunci: self.tampilkan_halaman(k),
                mode="terang", warna_teks=WARNA_TEKS,
                font=("Segoe UI", 14, "bold"),
                ikon=ikon, ikon_ukuran=18, ikon_warna=WARNA_AKSEN
            )
            tombol.pack(padx=20, pady=3)
            self.tombol_nav[kunci] = tombol

        TombolKaca(
            sidebar, "Logout", 200, 44, WARNA_BAHAYA,
            perintah=self.logout,
            mode="terang", warna_teks=WARNA_BAHAYA,
            font=("Segoe UI", 14, "bold"),
            ikon="daya", ikon_ukuran=18, ikon_warna=WARNA_BAHAYA
        ).pack(side="bottom", padx=20, pady=25)

    def buat_header(self, induk):
        header = ctk.CTkFrame(induk, fg_color="transparent")
        header.pack(fill="x", padx=35, pady=(28, 5))

        kiri = ctk.CTkFrame(header, fg_color="transparent")
        kiri.pack(side="left")

        self.label_judul_halaman = ctk.CTkLabel(
            kiri, text="Dashboard", font=FONT_JUDUL,
            text_color=WARNA_TEKS, anchor="w"
        )
        self.label_judul_halaman.pack(anchor="w")

        hari_ini = date.today()
        tanggal_teks = (
            f"{NAMA_HARI[hari_ini.weekday()]}, {hari_ini.day} "
            f"{NAMA_BULAN[hari_ini.month - 1]} {hari_ini.year}"
        )
        ctk.CTkLabel(
            kiri, text=tanggal_teks, font=FONT_KECIL,
            text_color=WARNA_TEKS_REDUP, anchor="w"
        ).pack(anchor="w")

        kanan = ctk.CTkFrame(header, fg_color="transparent")
        kanan.pack(side="right")

        nama = self.user["nama_lengkap"] if self.user else "Pengguna"
        inisial = "".join(k[0] for k in nama.split()[:2]).upper() or "U"

        ctk.CTkLabel(
            kanan, text=inisial, width=42, height=42, corner_radius=10,
            fg_color=WARNA_AKSEN_MUDA, text_color=WARNA_AKSEN,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")
        ctk.CTkLabel(
            kanan, text=nama, font=("Segoe UI", 13, "bold"),
            text_color=WARNA_TEKS
        ).pack(side="left", padx=(10, 0))

    def tampilkan_halaman(self, nama):
        self.halaman_dashboard.pack_forget()
        self.halaman_pengeluaran.pack_forget()

        if nama == "dashboard":
            self.halaman_dashboard.pack(fill="both", expand=True)
            judul = "Dashboard"
        else:
            self.halaman_pengeluaran.pack(fill="both", expand=True)
            judul = "Pengeluaran"

        self.label_judul_halaman.configure(text=judul)

        for kunci, tombol in self.tombol_nav.items():
            aktif = kunci == nama
            tombol.atur_gaya(
                mode="tebal" if aktif else "terang",
                warna_teks="#FFFFFF" if aktif else WARNA_TEKS,
                ikon_warna="#FFFFFF" if aktif else WARNA_AKSEN
            )

    def buka_form_baru(self):
        self.tampilkan_halaman("pengeluaran")
        self.bersihkan_form()
        self.input_nominal.focus()

    def _kartu_stat(self, induk, kolom, warna, warna_ikon, ikon, keterangan):
        try:
            sc = float(self._get_window_scaling())
        except Exception:
            sc = 1.0
        tinggi = int(round(88 * sc))

        rgb = ImageColor.getrgb(warna)
        terang = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) > 150
        warna_teks = WARNA_TEKS if terang else "#FFFFFF"
        warna_kotak = "#%02x%02x%02x" % _campur(rgb, (0, 0, 0), 0.16)

        font_nilai = tkfont.Font(
            family="Segoe UI", size=-int(round(18 * sc)), weight="bold"
        )
        font_ket = tkfont.Font(
            family="Segoe UI", size=-int(round(11 * sc))
        )

        kanvas = tk.Canvas(
            induk, height=tinggi, bg=WARNA_BG,
            highlightthickness=0, bd=0
        )
        kanvas.grid(
            row=0, column=kolom, sticky="ew",
            padx=(0 if kolom == 0 else 8, 0 if kolom == 3 else 8)
        )

        class _Nilai:
            def __init__(self):
                self.teks = "-"
                self.item = None

            def configure(self, **kw):
                if "text" in kw:
                    self.teks = kw["text"]
                    if self.item is not None:
                        kanvas.itemconfigure(self.item, text=self.teks)

        nilai = _Nilai()
        kanvas._gambar_ref = []
        lebar_terakhir = [0]

        def lukis(event=None):
            lebar = kanvas.winfo_width()
            if lebar < 40 or lebar == lebar_terakhir[0]:
                return
            lebar_terakhir[0] = lebar
            kanvas.delete("all")
            kanvas._gambar_ref = []

            def ke_foto(ctk_img, w, h):
                pil = getattr(ctk_img, "_light_image")
                pil = pil.resize((w, h), Image.LANCZOS)
                foto = ImageTk.PhotoImage(pil)
                kanvas._gambar_ref.append(foto)
                return foto

            latar = buat_gambar_kaca(
                lebar, tinggi, warna, "tebal", "normal",
                int(round(14 * sc))
            )
            kanvas.create_image(
                0, 0, anchor="nw", image=ke_foto(latar, lebar, tinggi)
            )

            ukuran = int(round(48 * sc))
            kotak = buat_gambar_kaca(
                ukuran, ukuran, warna_kotak, "tebal", "normal",
                int(round(12 * sc)), ikon,
                int(round(12 * sc)), int(round(24 * sc)), "#FFFFFF"
            )
            x_kotak = int(round(16 * sc))
            kanvas.create_image(
                x_kotak, (tinggi - ukuran) // 2, anchor="nw",
                image=ke_foto(kotak, ukuran, ukuran)
            )

            x_teks = x_kotak + ukuran + int(round(14 * sc))
            nilai.item = kanvas.create_text(
                x_teks, int(tinggi * 0.38), anchor="w",
                text=nilai.teks, fill=warna_teks, font=font_nilai
            )
            kanvas.create_text(
                x_teks, int(tinggi * 0.66), anchor="w",
                text=keterangan, fill=warna_teks, font=font_ket
            )

        kanvas.bind("<Configure>", lukis)
        return nilai

    def buat_halaman_dashboard(self):
        self.halaman_dashboard = ctk.CTkFrame(
            self.area, fg_color="transparent"
        )
        hal = self.halaman_dashboard

        banner = ctk.CTkFrame(hal, fg_color=WARNA_BANNER, corner_radius=18)
        banner.pack(fill="x", pady=(5, 22))

        teks = ctk.CTkFrame(banner, fg_color="transparent")
        teks.pack(side="left", padx=35, pady=32)

        nama_depan = (
            self.user["nama_lengkap"].split()[0] if self.user else "Pengguna"
        )
        ctk.CTkLabel(
            teks, text=f"Hai, {nama_depan}!", font=FONT_SAPA,
            text_color=WARNA_TEKS, anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(
            teks, text="Siap mencatat pengeluaranmu hari ini?",
            font=("Segoe UI", 14), text_color=WARNA_TEKS, anchor="w"
        ).pack(anchor="w", pady=(6, 0))

        logo = buat_logo(256)
        self.gambar_banner = ctk.CTkImage(
            light_image=logo, dark_image=logo, size=(104, 104)
        )
        ctk.CTkLabel(banner, text="", image=self.gambar_banner).pack(
            side="right", padx=45, pady=15
        )

        ctk.CTkLabel(
            hal, text="Ringkasan", font=FONT_LABEL,
            text_color=WARNA_TEKS_REDUP
        ).pack(anchor="w")

        baris = ctk.CTkFrame(hal, fg_color="transparent")
        baris.pack(fill="x", pady=(8, 22))
        for i in range(4):
            baris.grid_columnconfigure(i, weight=1, uniform="stat")

        self.nilai_bulan_ini = self._kartu_stat(
            baris, 0, "#F2C14E", "#F6D27C", "kalender", "Total Bulan Ini"
        )
        self.nilai_total = self._kartu_stat(
            baris, 1, "#4B3B9C", "#6A5BB4", "uang", "Total Keseluruhan"
        )
        self.nilai_transaksi = self._kartu_stat(
            baris, 2, "#E95D9A", "#EE82B2", "struk", "Jumlah Transaksi"
        )
        self.nilai_kategori = self._kartu_stat(
            baris, 3, "#BDB1E4", "#D2C9EF", "label", "Kategori Terbesar"
        )

        ctk.CTkLabel(
            hal, text="Pengeluaran Terbaru", font=FONT_LABEL,
            text_color=WARNA_TEKS_REDUP
        ).pack(anchor="w")

        self.daftar_terbaru = ctk.CTkFrame(hal, fg_color="transparent")
        self.daftar_terbaru.pack(fill="both", expand=True, pady=(6, 0))

    def perbarui_dashboard(self):
        data = self.data_pengeluaran
        bulan_ini = date.today().isoformat()[:7]

        total = sum(float(i["nominal"]) for i in data)
        total_bulan = sum(
            float(i["nominal"]) for i in data
            if str(i["tanggal"]).startswith(bulan_ini)
        )

        per_kategori = {}
        for i in data:
            per_kategori[i["nama_kategori"]] = (
                per_kategori.get(i["nama_kategori"], 0) + float(i["nominal"])
            )
        terbesar = (
            max(per_kategori, key=per_kategori.get) if per_kategori else "-"
        )

        self.nilai_bulan_ini.configure(text=f"Rp {total_bulan:,.0f}")
        self.nilai_total.configure(text=f"Rp {total:,.0f}")
        self.nilai_transaksi.configure(text=str(len(data)))
        self.nilai_kategori.configure(text=terbesar)

        for widget in self.daftar_terbaru.winfo_children():
            widget.destroy()

        if not data:
            ctk.CTkLabel(
                self.daftar_terbaru,
                text="Belum ada pengeluaran. Klik tombol ＋ untuk mulai mencatat.",
                font=("Segoe UI", 13), text_color=WARNA_TEKS_REDUP
            ).pack(anchor="w", pady=10)
            return

        for item in data[:5]:
            baris = ctk.CTkFrame(
                self.daftar_terbaru, fg_color=WARNA_KARTU, corner_radius=12
            )
            baris.pack(fill="x", pady=4)

            ctk.CTkLabel(
                baris, text=item["nama_kategori"], width=140, height=30,
                corner_radius=8, fg_color=WARNA_AKSEN_MUDA,
                text_color=WARNA_AKSEN, font=FONT_LABEL
            ).pack(side="left", padx=15, pady=12)

            info = ctk.CTkFrame(baris, fg_color="transparent")
            info.pack(side="left", pady=8)
            ctk.CTkLabel(
                info, text=item["deskripsi"] or "(tanpa deskripsi)",
                font=("Segoe UI", 13, "bold"), text_color=WARNA_TEKS,
                anchor="w"
            ).pack(anchor="w")
            ctk.CTkLabel(
                info, text=str(item["tanggal"]), font=FONT_KECIL,
                text_color=WARNA_TEKS_REDUP, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                baris, text=f"Rp {float(item['nominal']):,.0f}",
                font=("Segoe UI", 14, "bold"), text_color=WARNA_AKSEN
            ).pack(side="right", padx=20)

    def _tombol(self, induk, teks, warna, hover, perintah, ikon=None):
        TombolKaca(
            induk, teks, 130, 40, warna, perintah=perintah,
            ikon=ikon, ikon_ukuran=18
        ).pack(side="left", padx=(0, 10))

    def buat_halaman_pengeluaran(self):
        self.halaman_pengeluaran = ctk.CTkFrame(
            self.area, fg_color="transparent"
        )
        hal = self.halaman_pengeluaran

        form = ctk.CTkFrame(hal, fg_color=WARNA_KARTU, corner_radius=14)
        form.pack(fill="x", pady=(5, 10))

        form.grid_columnconfigure(1, weight=1)
        form.grid_columnconfigure(3, weight=1)

        self._label_form(form, "🏷  Kategori", 0, 0)
        self.pilih_kategori = KomboRapi(
            form, values=["Memuat kategori..."], width=250,
            **self._gaya_combo()
        )
        self.pilih_kategori.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew"
        )

        self._label_form(form, "📅  Tanggal (YYYY-MM-DD)", 0, 2)
        self.input_tanggal = ctk.CTkEntry(form, **self._gaya_entry())
        self.input_tanggal.grid(
            row=0, column=3, padx=(10, 20), pady=10, sticky="ew"
        )
        self.input_tanggal.insert(0, date.today().isoformat())

        self._label_form(form, "💰  Nominal (Rp)", 1, 0)
        self.input_nominal = ctk.CTkEntry(
            form, placeholder_text="Contoh: 25000", **self._gaya_entry()
        )
        self.input_nominal.grid(
            row=1, column=1, padx=10, pady=10, sticky="ew"
        )

        self._label_form(form, "📝  Deskripsi", 1, 2)
        self.input_deskripsi = ctk.CTkEntry(
            form, placeholder_text="Contoh: Makan siang",
            **self._gaya_entry()
        )
        self.input_deskripsi.grid(
            row=1, column=3, padx=(10, 20), pady=10, sticky="ew"
        )

        tombol = ctk.CTkFrame(hal, fg_color="transparent")
        tombol.pack(fill="x", pady=5)

        self._tombol(
            tombol, "Tambah", WARNA_AKSEN, WARNA_AKSEN_HOVER,
            self.tambah_data, ikon="tambah"
        )
        self._tombol(
            tombol, "Ubah", WARNA_AKSEN, WARNA_AKSEN_HOVER,
            self.ubah_data, ikon="pensil"
        )
        self._tombol(
            tombol, "Hapus", WARNA_BAHAYA, WARNA_BAHAYA_HOVER,
            self.hapus_data, ikon="sampah"
        )
        self._tombol(
            tombol, "Bersihkan", WARNA_NETRAL, WARNA_NETRAL_HOVER,
            self.bersihkan_form, ikon="segarkan"
        )

        filter_bar = ctk.CTkFrame(hal, fg_color="transparent")
        filter_bar.pack(fill="x", pady=(10, 0))

        kw_entry = self._gaya_entry()
        kw_entry["height"] = 36
        kw_combo = self._gaya_combo()
        kw_combo["height"] = 36

        self.input_cari = ctk.CTkEntry(
            filter_bar, width=240,
            placeholder_text="🔍  Cari deskripsi atau kategori...",
            **kw_entry
        )
        self.input_cari.pack(side="left", padx=(0, 10))
        self.input_cari.bind(
            "<KeyRelease>", lambda event: self.terapkan_filter()
        )

        self.filter_kategori = KomboRapi(
            filter_bar, width=190, values=["Semua kategori"],
            state="readonly",
            command=lambda nilai: self.terapkan_filter(),
            **kw_combo
        )
        self.filter_kategori.set("Semua kategori")
        self.filter_kategori.pack(side="left", padx=10)

        self.filter_bulan = KomboRapi(
            filter_bar, width=160, values=["Semua bulan"],
            state="readonly",
            command=lambda nilai: self.terapkan_filter(),
            **kw_combo
        )
        self.filter_bulan.set("Semua bulan")
        self.filter_bulan.pack(side="left", padx=10)

        TombolKaca(
            filter_bar, "Ekspor CSV", 140, 36, WARNA_NETRAL,
            perintah=self.ekspor_csv, ikon="unduh", ikon_ukuran=16
        ).pack(side="left", padx=10)

        self.label_ringkasan = ctk.CTkLabel(
            filter_bar, text="Total: Rp 0   •   0 transaksi",
            font=FONT_LABEL, text_color=WARNA_TEKS
        )
        self.label_ringkasan.pack(side="right")

        tabel_frame = ctk.CTkFrame(
            hal, fg_color=WARNA_KARTU, corner_radius=14
        )
        tabel_frame.pack(fill="both", expand=True, pady=(10, 0))

        kolom = (
            "id", "tanggal", "nama_user",
            "kategori", "nominal", "deskripsi"
        )

        self.tabel = ttk.Treeview(
            tabel_frame, columns=kolom, show="headings"
        )

        self.tabel.tag_configure("baris_a", background=WARNA_BARIS_A)
        self.tabel.tag_configure("baris_b", background=WARNA_BARIS_B)

        judul_kolom = {
            "id": "ID",
            "tanggal": "Tanggal",
            "nama_user": "Pengguna",
            "kategori": "Kategori",
            "nominal": "Nominal (Rp)",
            "deskripsi": "Deskripsi"
        }

        lebar_kolom = {
            "id": 50,
            "tanggal": 110,
            "nama_user": 170,
            "kategori": 150,
            "nominal": 120,
            "deskripsi": 200
        }

        rata_kolom = {
            "id": "center",
            "tanggal": "center",
            "nama_user": "w",
            "kategori": "w",
            "nominal": "e",
            "deskripsi": "w"
        }

        for kolom_id in kolom:
            self.tabel.heading(
                kolom_id, text=judul_kolom[kolom_id]
            )
            self.tabel.column(
                kolom_id,
                width=lebar_kolom[kolom_id],
                anchor=rata_kolom[kolom_id]
            )

        scrollbar = ttk.Scrollbar(
            tabel_frame, orient="vertical",
            command=self.tabel.yview
        )
        self.tabel.configure(yscrollcommand=scrollbar.set)

        self.tabel.pack(
            side="left", fill="both", expand=True, padx=(12, 0), pady=12
        )
        scrollbar.pack(side="right", fill="y", padx=(4, 12), pady=12)

        self.tabel.bind(
            "<<TreeviewSelect>>", self.pilih_baris
        )

    def muat_pilihan(self):
        self.data_kategori = get_all_kategori()

        daftar_kategori = [
            f"{k['id_kategori']} - {k['nama_kategori']}"
            for k in self.data_kategori
        ]

        self.pilih_kategori.configure(
            values=daftar_kategori or ["Tidak ada kategori"]
        )
        self.filter_kategori.configure(
            values=["Semua kategori"] + [
                k["nama_kategori"] for k in self.data_kategori
            ]
        )

        if daftar_kategori:
            self.pilih_kategori.set(daftar_kategori[0])

    def ambil_input(self):
        kategori = self.pilih_kategori.get()
        tanggal = self.input_tanggal.get().strip()
        nominal_teks = self.input_nominal.get().strip()
        deskripsi = self.input_deskripsi.get().strip()

        if kategori.startswith("Tidak ada") or not kategori:
            messagebox.showwarning(
                "Peringatan", "Pilih kategori terlebih dahulu."
            )
            return None

        try:
            id_kategori = int(kategori.split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showwarning(
                "Peringatan", "Pilihan kategori tidak valid."
            )
            return None

        try:
            tanggal_obj = date.fromisoformat(tanggal)
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Tanggal harus menggunakan format YYYY-MM-DD."
            )
            return None

        if tanggal_obj.isoformat() != tanggal:
            messagebox.showwarning(
                "Peringatan",
                "Masukkan tanggal yang valid dengan format YYYY-MM-DD."
            )
            return None

        try:
            nominal_bersih = bersihkan_nominal(nominal_teks)
            nominal = float(nominal_bersih)
            if nominal <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Peringatan", "Nominal harus berupa angka lebih dari 0."
            )
            return None

        return (
            id_kategori,
            tanggal,
            nominal,
            deskripsi
        )

    def tampilkan_data(self):
        self.data_pengeluaran = self.controller.tampilkan_pengeluaran()

        bulan_ada = sorted(
            {str(item["tanggal"])[:7] for item in self.data_pengeluaran},
            reverse=True
        )
        pilihan_bulan = ["Semua bulan"] + bulan_ada
        self.filter_bulan.configure(values=pilihan_bulan)
        if self.filter_bulan.get() not in pilihan_bulan:
            self.filter_bulan.set("Semua bulan")

        self.perbarui_dashboard()
        self.terapkan_filter()

    def terapkan_filter(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        kata = self.input_cari.get().strip().lower()
        kategori = self.filter_kategori.get()
        bulan = self.filter_bulan.get()

        total = 0.0
        jumlah = 0
        id_tampil = []

        for item in self.data_pengeluaran:
            deskripsi = item["deskripsi"] or ""

            if kategori != "Semua kategori" and item["nama_kategori"] != kategori:
                continue

            if bulan != "Semua bulan" and not str(item["tanggal"]).startswith(bulan):
                continue

            if kata and kata not in deskripsi.lower() \
                    and kata not in item["nama_kategori"].lower():
                continue

            self.tabel.insert(
                "",
                "end",
                values=(
                    item["id_pengeluaran"],
                    item["tanggal"],
                    item["nama_user"],
                    item["nama_kategori"],
                    f"{float(item['nominal']):,.0f}",
                    deskripsi
                ),
                tags=("baris_a" if jumlah % 2 == 0 else "baris_b",)
            )

            total += float(item["nominal"])
            jumlah += 1
            id_tampil.append(item["id_pengeluaran"])

        if self.id_terpilih not in id_tampil:
            self.id_terpilih = None

        self.label_ringkasan.configure(
            text=f"Total: Rp {total:,.0f}   •   {jumlah} transaksi"
        )

    def ekspor_csv(self):
        baris = [
            self.tabel.item(item, "values")
            for item in self.tabel.get_children()
        ]

        if not baris:
            messagebox.showwarning(
                "Peringatan", "Tidak ada data untuk diekspor."
            )
            return

        lokasi = filedialog.asksaveasfilename(
            title="Simpan data pengeluaran",
            defaultextension=".csv",
            initialfile=f"pengeluaran_{date.today().isoformat()}.csv",
            filetypes=[("File CSV", "*.csv")]
        )

        if not lokasi:
            return

        try:
            with open(lokasi, "w", newline="", encoding="utf-8-sig") as f:
                penulis = csv.writer(f)
                penulis.writerow(
                    ["ID", "Tanggal", "Pengguna", "Kategori",
                     "Nominal (Rp)", "Deskripsi"]
                )
                for nilai in baris:
                    penulis.writerow(
                        [nilai[0], nilai[1], nilai[2], nilai[3],
                         str(nilai[4]).replace(",", ""), nilai[5]]
                    )

            messagebox.showinfo(
                "Berhasil", f"Data berhasil diekspor ke:\n{lokasi}"
            )
        except OSError as e:
            messagebox.showerror("Gagal", f"Data gagal diekspor: {e}")

    def tambah_data(self):
        data = self.ambil_input()
        if data is None:
            return

        berhasil = self.controller.tambah(*data)

        if berhasil:
            messagebox.showinfo(
                "Berhasil", "Pengeluaran berhasil ditambahkan."
            )
            self.bersihkan_form()
            self.tampilkan_data()
        else:
            messagebox.showerror(
                "Gagal", "Pengeluaran gagal ditambahkan."
            )

    def pilih_baris(self, event=None):
        pilihan = self.tabel.selection()
        if not pilihan:
            return

        nilai = self.tabel.item(pilihan[0], "values")
        self.id_terpilih = int(nilai[0])

        self.input_tanggal.delete(0, tk.END)
        self.input_tanggal.insert(0, str(nilai[1]))

        self.input_nominal.delete(0, tk.END)
        self.input_nominal.insert(
            0, str(nilai[4]).replace(",", "")
        )

        self.input_deskripsi.delete(0, tk.END)
        self.input_deskripsi.insert(0, str(nilai[5]))

        for k in self.data_kategori:
            if k["nama_kategori"] == nilai[3]:
                self.pilih_kategori.set(
                    f"{k['id_kategori']} - {k['nama_kategori']}"
                )
                break

    def ubah_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan", "Pilih data pada tabel yang ingin diubah."
            )
            return

        data = self.ambil_input()
        if data is None:
            return

        berhasil = self.controller.ubah(self.id_terpilih, *data)

        if berhasil:
            messagebox.showinfo(
                "Berhasil", "Pengeluaran berhasil diubah."
            )
            self.bersihkan_form()
            self.tampilkan_data()
        else:
            messagebox.showwarning(
                "Informasi",
                "Data tidak berubah atau gagal diubah."
            )

    def hapus_data(self):
        if self.id_terpilih is None:
            messagebox.showwarning(
                "Peringatan", "Pilih data pada tabel yang ingin dihapus."
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin menghapus pengeluaran ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.controller.hapus(self.id_terpilih)

        if berhasil:
            messagebox.showinfo(
                "Berhasil", "Pengeluaran berhasil dihapus."
            )
            self.bersihkan_form()
            self.tampilkan_data()
        else:
            messagebox.showerror(
                "Gagal", "Pengeluaran gagal dihapus."
            )

    def logout(self):
        konfirmasi = messagebox.askyesno(
            "Konfirmasi", "Apakah kamu yakin ingin keluar dari akun?"
        )

        if not konfirmasi:
            return

        self.keluar_akun = True
        self.destroy()

    def bersihkan_form(self):
        self.id_terpilih = None

        self.input_tanggal.delete(0, tk.END)
        self.input_tanggal.insert(0, date.today().isoformat())

        self.input_nominal.delete(0, tk.END)
        self.input_deskripsi.delete(0, tk.END)

        if self.data_kategori:
            k = self.data_kategori[0]
            self.pilih_kategori.set(
                f"{k['id_kategori']} - {k['nama_kategori']}"
            )

        for item in self.tabel.selection():
            self.tabel.selection_remove(item)