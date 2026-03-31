
import csv
from csv_definialas import Etel, Asztal
 
class EtteremRendszer:
    """
    Egyszerű étterem-kezelő osztály.
 
    Paraméterek:
    - asztalok_szama (int): hány asztalt hozzon létre az étterem.
 
    A példány mezői:
    - self.asztalok: Asztal objektumok listája.
    - self.menu: név -> Etel objektum (ár, receptek).
    - self.raktar: alapanyag -> mennyiség (float).
    """
 
    def __init__(self, asztalok_szama):
        # Létrehozzuk az asztalokat és elmentjük őket listába.
        self.asztalok = []
        for i in range(asztalok_szama):
            uj_asztal = Asztal(i + 1)
            self.asztalok.append(uj_asztal)
 
        # Menü és raktár kezdetben üres
        self.menu = {}
        self.raktar = {}
        # Beolvassuk a fájlokat
        self.betoltes()
 
    def betoltes(self):
        """
        Beolvassa a raktár, receptek és menü adatait CSV fájlokból.
        Fájlok:
        - raktar.csv: alapanyag;mennyiseg
        - recept.csv: etel_nev;alapanyag;mennyiseg
        - menu.csv: etel_nev;ar
        """
        # Raktár beolvasása
        with open('raktar.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                # sor[0] = alapanyag neve, sor[1] = mennyiség
                self.raktar[sor[0]] = float(sor[1])
 
        # Receptek beolvasása: receptek[etel_nev] = {alapanyag: mennyiseg, ...}
        receptek = {}
        with open('recept.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                etel_nev, alapanyag, mennyiseg = sor[0], sor[1], float(sor[2])
                if etel_nev not in receptek:
                    receptek[etel_nev] = {}
                receptek[etel_nev][alapanyag] = mennyiseg
 
        # Menü beolvasása és Etel objektumok létrehozása
        with open('menu.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                nev, ar = sor[0], int(sor[1])
                # Ha nincs recept egy ételhez, üres dictet adunk
                self.menu[nev] = Etel(nev, ar, receptek.get(nev, {}))
 
    def rendeles_felvetel(self, asztal_szam, etel_nev):
        """
        Felvesz egy rendelést az adott asztalhoz.
 
        Visszatérési érték:
        - sikeres felvétel esetén: "Rendelés hozzáadva!"
        - ha nincs ilyen étel: "Nincs ilyen étel az étlapon!"
        - ha nincs elég alapanyag: "Nincs elég alapanyag: <alapanyag>"
        """
        etel = self.menu.get(etel_nev)
        if not etel:
            return "Nincs ilyen étel az étlapon!"
 
        # Ellenőrizzük, hogy van-e elég alapanyag minden hozzávalóból
        for alapanyag, mennyiseg in etel.receptek.items():
            if self.raktar.get(alapanyag, 0) < mennyiseg:
                return f"Nincs elég alapanyag: {alapanyag}"
 
        # Levonjuk az alapanyagokat a raktárból
        for alapanyag, mennyiseg in etel.receptek.items():
            self.raktar[alapanyag] -= mennyiseg
 
        # Hozzáadjuk az ételt az asztal rendeléséhez
        self.asztalok[asztal_szam - 1].hozzaad(etel)
        return "Rendelés hozzáadva!"
 
    def fizetes(self, asztal_szam, vasarlo_neve, kiszolgalo_neve):
        """
        Lezárja az asztal rendelését, visszaadja az összeget és rögzíti a vásárlást.
 
        Visszatérési érték:
        - ha nincs aktív rendelés: "Az asztalnál nincs aktív rendelés."
        - sikeres fizetés esetén: "Fizetve: <osszeg> Ft. Köszönjük!"
        """
        asztal = self.asztalok[asztal_szam - 1]
        if not asztal.nyitva:
            return "Az asztalnál nincs aktív rendelés."
 
        # asztal.lezaras() feltételezhetően visszaadja: (osszeg, tetel_lista)
        osszeg, tetelek = asztal.lezaras()
 
        # Statisztika: hány darab volt egy-egy tételből
        tetel_statisztika = {}
        for etel in tetelek:
            tetel_statisztika[etel] = tetel_statisztika.get(etel, 0) + 1
 
        tetel_string = ", ".join([f"{k} ({v}x)" for k, v in tetel_statisztika.items()])
 
        # Vásárlás rögzítése CSV-be
        with open('vasarlasok.csv', 'a', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            iro.writerow([vasarlo_neve, kiszolgalo_neve, osszeg, tetel_string])
 
        return f"Fizetve: {osszeg} Ft. Köszönjük!"
