# Ez a fájl kezeli:
# - CSV-k beolvasása/mentése
# - étlap és receptek kezelése
# - raktárkészlet (azonnali csökkentés rendeléskor)
# - rendelés felvétel és fizetés
# - vásárlások rögzítése CSV-be


import csv
from csv_definialas import Etel, Asztal


class EtteremRendszer:
    """
    - self.asztalok: Asztal objektumok listája (index: asztal_szam-1)
    - self.menu: név -> Etel
    - self.raktar: alapanyag -> mennyiség (float)
    """

    def __init__(self, asztalok_szama):
        # Asztalok létrehozása (1..asztalok_szama)
        self.asztalok = []
        i = 1
        while i <= asztalok_szama:
            self.asztalok.append(Asztal(i))
            i += 1

        self.menu = {}
        self.raktar = {}

        # Betöltjük a CSV-ket
        self.betoltes()

    def betoltes(self):
        # Raktár beolvasása
        try:
            with open('raktar.csv', 'r', encoding='utf-8') as f:
                olvaso = csv.reader(f, delimiter=';')
                for sor in olvaso:
                    if not sor:
                        continue
                    alapanyag = sor[0]
                    menny = float(sor[1])
                    self.raktar[alapanyag] = menny
            self.raktar = {}

        # Receptek ideiglenes gyűjtése: etel_nev -> {alapanyag: mennyiség}
        receptek = {}
        try:
            with open('recept.csv', 'r', encoding='utf-8') as f:
                olvaso = csv.reader(f, delimiter=';')
                for sor in olvaso:
                    if not sor:
                        continue
                    etel_nev = sor[0]
                    alapanyag = sor[1]
                    menny = float(sor[2])
                    if etel_nev not in receptek:
                        receptek[etel_nev] = {}
                    receptek[etel_nev][alapanyag] = menny
        except FileNotFoundError:
            receptek = {}

        # Menü beolvasása és Etel objektumok létrehozása
        try:
            with open('menu.csv', 'r', encoding='utf-8') as f:
                olvaso = csv.reader(f, delimiter=';')
                for sor in olvaso:
                    if not sor:
                        continue
                    nev = sor[0]
                    ar = int(sor[1])
                    self.menu[nev] = Etel(nev, ar, receptek.get(nev, {}))
            self.menu = {}
====

    def ment_raktar(self):
        # Raktár mentése (abc sorrendben)
        with open('raktar.csv', 'w', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            for alapanyag in sorted(self.raktar.keys()):
                iro.writerow([alapanyag, self.raktar[alapanyag]])

    def ment_menu_es_receptek(self):
        # Menü mentése
        with open('menu.csv', 'w', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            for nev in sorted(self.menu.keys()):
                etel = self.menu[nev]
                iro.writerow([etel.nev, etel.ar])

        # Receptek mentése (minden étel összes hozzávalója külön sor)
        with open('recept.csv', 'w', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            for nev in sorted(self.menu.keys()):
                etel = self.menu[nev]
                for alapanyag in etel.receptek:
                    menny = etel.receptek[alapanyag]
                    iro.writerow([nev, alapanyag, menny])


    def valid_asztal(self, asztal_szam):
        return 1 <= asztal_szam <= len(self.asztalok)

    def keres_etel_kulcs(self, etel_nev):
        for nev in self.menu:
            if nev.lower() == etel_nev.lower():
                return nev
        return None

    def rendelheto_e(self, etel):
        # Megnézzük, minden alapanyagból van-e elég.
        for alapanyag in etel.receptek:
            kell = etel.receptek[alapanyag]
            if self.raktar.get(alapanyag, 0.0) < kell:
                return False
        return True

    def hianyok(self, etel):
        # Megnézzük, miből mennyi hiányzik (ha nincs készleten, a teljes kell mennyisége hiány).
        h = {}
        for alapanyag in etel.receptek:
            kell = etel.receptek[alapanyag]
            megvan = self.raktar.get(alapanyag, 0.0)
            if megvan < kell:
                h[alapanyag] = kell - megvan
        return h

    def anyag_felhasznal(self, etel):
        # Ha rendelhető, levonjuk a raktárból a mennyiségeket.
        for alapanyag in etel.receptek:
            self.raktar[alapanyag] = self.raktar.get(alapanyag, 0.0) - etel.receptek[alapanyag]


    def rendeles_felvetel(self, asztal_szam, etel_nev):
        """
        Rendelés felvétele egy asztalhoz.
        - Ha nincs ilyen asztal: hibaüzenet.
        - Ha nincs ilyen étel: hibaüzenet.
        - Ha nincs elég alapanyag: pontos hiánylista.
        - Ha sikerül: azonnal csökken a raktár, és az asztal rendelésébe kerül az étel.
        """
        if not self.valid_asztal(asztal_szam):
            return "Nincs ilyen asztal: " + str(asztal_szam) + " (érvényes: 1.." + str(len(self.asztalok)) + ")"

        kulcs = self.keres_etel_kulcs(etel_nev)
        if kulcs is None:
            return "Nincs ilyen étel az étlapon!"

        etel = self.menu[kulcs]

        if not self.rendelheto_e(etel):
            # Hiányok kiírása (számlálás/jegyzés tétel)
            h = self.hianyok(etel)
            uzenet = "Nincs elég alapanyag: "
            elso = True
            for alapanyag in h:
                if not elso:
                    uzenet += ", "
                uzenet += alapanyag + " (hiányzik " + format(h[alapanyag], ".3f") + ")"
                elso = False
            return uzenet

        # Raktár csökkentése és asztalhoz adás
        self.anyag_felhasznal(etel)
        self.asztalok[asztal_szam - 1].hozzaad(etel)

        # Raktár azonnali mentése, hogy tartós legyen
        self.ment_raktar()

        return "Rendelés hozzáadva!"

    def fizetes(self, asztal_szam, vasarlo_neve, kiszolgalo_neve):
        """
        Lezárja az asztalt, összegzi a rendelést, és menti a vasarlasok.csv-be.
        A tételek darabszámmal szerepelnek (pl. 'Cola (5x)').
        """
        if not self.valid_asztal(asztal_szam):
            return "Nincs ilyen asztal: " + str(asztal_szam) + " (érvényes: 1.." + str(len(self.asztalok)) + ")"

        asztal = self.asztalok[asztal_szam - 1]
        if not asztal.nyitva:
            return "Az asztalnál nincs aktív rendelés."

        # Asztal lezárása: (összegzés tétele + lista)
        osszeg, nevek = asztal.lezaras()

        # Számlálás tétele: nevek darabjainak összeszámolása
        tetel_statisztika = {}
        for nev in nevek:
            tetel_statisztika[nev] = tetel_statisztika.get(nev, 0) + 1

        # Formázott tétellista: "Pizza (2x), Cola (1x)"
        parok = []
        for nev in tetel_statisztika:
            parok.append(nev + " (" + str(tetel_statisztika[nev]) + "x)")
        tetel_string = ", ".join(parok)

        # Vásárlás rögzítése
        with open('vasarlasok.csv', 'a', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            iro.writerow([vasarlo_neve, kiszolgalo_neve, osszeg, tetel_string])

        return "Fizetve: " + str(osszeg) + " Ft. Köszönjük!"


    def etel_hozzaad(self, nev, ar, hozzavalok):
        """
        Új étel felvétele az étlapra.
        - nev: string
        - ar: int
        - hozzavalok: dict (alapanyag -> mennyiség float)

        Mentés: menu.csv + recept.csv frissül.
        """
        if nev in self.menu:
            return "Már van ilyen nevű étel az étlapon."

        # Új Etel létrehozása és hozzáadása
        self.menu[nev] = Etel(nev, ar, hozzavalok)

        # Menü+recept mentése
        self.ment_menu_es_receptek()
        return "Új étel felvéve az étlapra: " + nev

    def etel_torles(self, nev):
        """
        Étel törlése név alapján az étlapról.
        A hozzá tartozó receptek is törlődnek (mentéskor).
        """
        kulcs = self.keres_etel_kulcs(nev)
        if kulcs is None:
            return "Nincs ilyen étel az étlapon."

        # Töröljük a menüből
        del self.menu[kulcs]

        # Menü+recept mentése
        self.ment_menu_es_receptek()
        return "Étel törölve: " + nev
``
