# Rickov rojstni dan

Interaktivna rojstnodnevna igra s temo Formule 1, v slovenščini. Pet preizkusov,
na koncu Max Verstappen pove, kje je skrito darilo.

Vse skupaj je ena sama datoteka `index.html` (HTML, CSS in JavaScript),
brez npm, brez gradnje in brez odvisnosti. Grafika je pixel art, narisan
na canvas, zvočni efekti pa nastajajo sproti prek Web Audio API.

## Zagon

Odpri `index.html` v brskalniku. Za glasbo v ozadju priporočam lokalni strežnik:

    python -m http.server 8765

Nato odpri `http://localhost:8765`.

## Igre

| # | Igra | Kaj moraš narediti |
|---|---|---|
| 1 | Lovi senco | Ostani pod premikajočo se senco 10 sekund, časa imaš 40 sekund |
| 2 | F1 kviz | Pet vprašanj, en napačen odgovor pomeni konec |
| 3 | Perfect start | Ko ugasnejo startne luči, pritisni v 250 ms |
| 4 | Pit stop | Vsako od štirih koles pritisni trikrat, vse skupaj pod 3,2 sekunde |
| 5 | Drži vodstvo | Petnajst sekund blokiraj tri nasprotnike, na voljo imaš 4 sekunde boosta |

Vseh pet je treba rešiti v enem poskusu. Ob tretjem porazu se pojavi Lance Stroll,
ob vsakem petem pa parada formul z Maxom.

## Nastavitve

Na vrhu skripte v `index.html` je blok z nastavitvami:

- `GIFT_LOCATION` — kje je skrito darilo, to je treba vpisati pred igranjem
- `QUIZ` — vprašanja kviza, polje `a` je indeks pravilnega odgovora
- `BG_MUSIC` in `BG_VOLUME` — glasba v ozadju

Drugje v kodi: vrstni red iger določa `ORDER`, pravila so v `renderHub()`,
trajanje parade pa je konstanta `PARADE_SEC`.

## Testiranje

Posamezno igro odpreš naravnost prek naslova, na primer `index.html?test=3`.
Številke so 0 za Perfect start, 1 za Lovi senco, 2 za kviz, 3 za Drži vodstvo
in 4 za Pit stop. V konzoli brskalnika te `go('final')` odpelje na zaključni
zaslon, `fails = 2; loseGame('test')` pa pokaže Lancea.

## Vsebina

Slike dirkačev in priložena glasba so uporabljene samo za osebno,
nekomercialno rojstnodnevno darilo. Avtorske pravice pripadajo njihovim lastnikom.
