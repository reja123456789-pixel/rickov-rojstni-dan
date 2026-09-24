import segno
from PIL import Image, ImageDraw, ImageFont

URL = "https://drive.google.com/file/d/1Mvs4MHRQAJwymKJlaQlvIoPvHhBnqHV-/view?usp=sharing"

DPI = 300
W, H = 2480, 3508                      # A4 pri 300 dpi
NIGHT, INK, GOLD, GOLD_D = "#1b1d3a", "#f4f0e6", "#ffd23f", "#a8850e"
RED, DARK = "#e63946", "#0b0c1e"
WOOD_D, WOOD, WOOD_L = "#6b3312", "#8b4a1f", "#a35c28"
STAR = "\u2605"

def font(sz):
    for f in ("C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try: return ImageFont.truetype(f, sz)
        except OSError: pass
    return ImageFont.load_default()

def symfont(sz):
    try: return ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", sz)
    except OSError: return font(sz)

def page():
    im = Image.new("RGB", (W, H), NIGHT)
    d = ImageDraw.Draw(im)
    s = 78                                   # velikost kvadratka sahovnice
    for i in range(W // s + 1):
        for j in range(2):
            c = INK if (i + j) % 2 else DARK
            d.rectangle([i*s, j*s, i*s+s-1, j*s+s-1], fill=c)
            d.rectangle([i*s, H-2*s+j*s, i*s+s-1, H-2*s+j*s+s-1], fill=c)
    return im, d

def center(d, t, y, fnt, fill, shadow=None):
    w = d.textbbox((0, 0), t, font=fnt)[2]
    x = (W - w) // 2
    if shadow:
        o = max(3, fnt.size // 14)
        d.text((x+o, y+o), t, font=fnt, fill=shadow)
    d.text((x, y), t, font=fnt, fill=fill)

def center_stars(d, txt, y, size, tcol):
    tf, sf = font(size), symfont(size)
    tb = d.textbbox((0,0), txt, font=tf); sb = d.textbbox((0,0), STAR, font=sf)
    tw, sw = tb[2], sb[2]
    dy = round(((tb[1]+tb[3]) - (sb[1]+sb[3])) / 2)
    gap = size // 2
    x = (W - (sw + gap + tw + gap + sw)) // 2
    d.text((x, y+dy), STAR, font=sf, fill=GOLD); x += sw + gap
    d.text((x, y), txt, font=tf, fill=tcol);     x += tw + gap
    d.text((x, y+dy), STAR, font=sf, fill=GOLD)

# ---------- pixel art skrinja ----------
def chest(d, ox, oy, S, odprta=False):
    """Skrinja v mrezi 44 x 34 enot, ox/oy je zgornji levi kot."""
    def px(x, y, w, h, c):
        d.rectangle([ox+x*S, oy+y*S, ox+(x+w)*S-1, oy+(y+h)*S-1], fill=c)

    pokrov = [(0,4,40),(1,3,41),(2,2,42),(3,1,43)] + [(y,0,44) for y in range(4,14)]
    telo   = [(y,0,44) for y in range(15,31)]
    if odprta:
        pokrov = [(y-5, x0, x1) for (y, x0, x1) in pokrov]     # dvignjen pokrov

    for y, x0, x1 in pokrov + telo:           # temna silhueta
        px(x0, y, x1-x0, 1, DARK)
    px(-1, 31, 46, 3, DARK)                   # podstavek

    def notranjost(vrste, barva):
        for y, x0, x1 in vrste:
            gor  = (y-1, x0, x1) not in vrste and not any(v[0]==y-1 for v in vrste)
            dol  = not any(v[0]==y+1 for v in vrste)
            if gor or dol: continue
            px(x0+1, y, x1-x0-2, 1, barva)

    notranjost(pokrov, WOOD)
    notranjost(telo, WOOD)
    ys_p = [v[0] for v in pokrov]; ys_t = [v[0] for v in telo]
    px(2, min(ys_p)+2, 40, 1, WOOD_L)                      # svetel odsev na pokrovu
    px(1, max(ys_t)-2, 42, 2, WOOD_D)                      # senca ob dnu

    if odprta:                                              # odprta skrinja: notranjost in zlato
        g0, g1 = max(ys_p)+1, min(ys_t)-1
        px(1, g0, 42, g1-g0+1, DARK)                        # senca v skrinji
        px(2, g0, 3, g1-g0+1, WOOD_D)                       # notranja stena levo
        px(39, g0, 3, g1-g0+1, WOOD_D)                      # notranja stena desno
        px(5, g1-2, 34, 3, GOLD)                            # kup zlata
        px(9, g1-4, 26, 2, "#fff3a0")
        px(15, g1-5, 14, 1, GOLD)
        px(1, min(ys_t), 42, 2, GOLD)                       # svetel rob telesa

    for bx in (5, 33):                                      # navpicni zlati trakovi
        px(bx-1, min(ys_p), 8, max(ys_p)-min(ys_p)+1, DARK)
        px(bx,   min(ys_p), 6, max(ys_p)-min(ys_p)+1, GOLD)
        px(bx+4, min(ys_p), 2, max(ys_p)-min(ys_p)+1, GOLD_D)
        px(bx-1, min(ys_t), 8, max(ys_t)-min(ys_t)+1, DARK)
        px(bx,   min(ys_t), 6, max(ys_t)-min(ys_t)+1, GOLD)
        px(bx+4, min(ys_t), 2, max(ys_t)-min(ys_t)+1, GOLD_D)

    px(0, max(ys_p)-2, 44, 3, DARK)                         # vodoravni trak pod pokrovom
    px(0, max(ys_p)-1, 44, 1, GOLD)

    if not odprta:                                          # kljucavnica le na zaprti skrinji
        lock_y = max(ys_p)
        px(18, lock_y-1, 8, 9, DARK)
        px(19, lock_y,   6, 7, GOLD)
        px(21, lock_y+2, 2, 2, DARK)
        px(21, lock_y+4, 2, 2, DARK)

def iskrice(d, ox, oy, S, tocke):
    for (x, y, r) in tocke:
        X, Y = ox+x*S, oy+y*S
        d.rectangle([X-r*S//3, Y-S//6, X+r*S//3, Y+S//6], fill=GOLD)
        d.rectangle([X-S//6, Y-r*S//3, X+S//6, Y+r*S//3], fill=GOLD)

# ================= STRAN 1: ZUNANJA =================
im1, d1 = page()
center_stars(d1, "GRAND PRIX RICK 28", 330, 74, RED)
center(d1, "ZAKLAD", 520, font(200), GOLD, DARK)

S = 42
CW, CH = 44*S, 34*S
ox, oy = (W - CW)//2, 1080
d1.ellipse([ox-120, oy+CH-260, ox+CW+120, oy+CH+180], fill="#22254a")   # sij pod skrinjo
chest(d1, ox, oy, S)
iskrice(d1, ox, oy, S, [(-5,4,3),(49,8,4),(-7,20,2),(51,24,3),(-3,30,2),(47,31,3),(-6,13,3),(50,15,2)])

center(d1, "ODPRI ME", 2780, font(130), INK, DARK)
center(d1, "notri te čaka skriti posnetek", 2960, font(52), "#9aa0c8")
im1.save("zaklad-zunaj.png")

# ================= STRAN 2: NOTRANJA =================
im2, d2 = page()
center(d2, "POGLEJ DO KONCA", 320, font(150), GOLD, DARK)
center(d2, "skeniraj kodo s telefonom", 540, font(52), "#9aa0c8")

# QR: najprej en piksel na kvadratek, nato povecava za cel veckratnik,
# da noben kvadratek ni popacen in koda ostane berljiva
qr = segno.make(URL, error="h")
qr.save("_qr_zaklad.png", scale=1, border=3, dark=DARK, light=INK)
base = Image.open("_qr_zaklad.png").convert("RGB")
faktor = 1400 // base.width
QS = base.width * faktor
q = base.resize((QS, QS), Image.NEAREST)
qx, qy = (W-QS)//2, 700
print(f"QR: {base.width} kvadratkov, faktor {faktor}, koncno {QS} px")
d2.rectangle([qx-34, qy-34, qx+QS+33, qy+QS+33], fill=GOLD)
d2.rectangle([qx-14, qy-14, qx+QS+13, qy+QS+13], fill=DARK)
im2.paste(q, (qx, qy))

S2 = 20
CW2 = 44*S2
ox2, oy2 = (W-CW2)//2, 2310
chest(d2, ox2, oy2, S2, odprta=True)
iskrice(d2, ox2, oy2, S2, [(-7,6,3),(51,8,3),(-5,22,2),(49,24,3),(-9,14,2),(53,16,2)])

center_stars(d2, "VSE NAJBOLJŠE RICK", 3130, 70, INK)
im2.save("zaklad-notri.png")

im1.save("zaklad-a4.pdf", "PDF", resolution=float(DPI), save_all=True, append_images=[im2])
import os; os.remove("_qr_zaklad.png")
print("narejeno")
