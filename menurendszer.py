import csv
from csv_definialas import Etel, Asztal


class EtteremRendszer:
    def __init__(self, asztalok_szama):
        self.asztalok = [Asztal(i + 1) for i in range(asztalok_szama)]
        self.menu = {}
        self.raktar = {}
        self.betoltes()

    def betoltes(self):
        with open('raktar.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                self.raktar[sor[0]] = float(sor[1])

        receptek = {}
        with open('recept.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                if sor[0] not in receptek:
                    receptek[sor[0]] = {}
                receptek[sor[0]][sor[1]] = float(sor[2])

        with open('menu.csv', 'r', encoding='utf-8') as f:
            for sor in csv.reader(f, delimiter=';'):
                nev, ar = sor[0], int(sor[1])
                self.menu[nev] = Etel(nev, ar, receptek.get(nev, {}))

    def rendeles_felvetel(self, asztal_szam, etel_nev):
        etel = self.menu.get(etel_nev)
        if not etel:
            return "Nincs ilyen étel az étlapon!"

        for alapanyag, mennyiseg in etel.receptek.items():
            if self.raktar.get(alapanyag, 0) < mennyiseg:
                return f"Nincs elég alapanyag: {alapanyag}"

        for alapanyag, mennyiseg in etel.receptek.items():
            self.raktar[alapanyag] -= mennyiseg

        self.asztalok[asztal_szam - 1].hozzaad(etel)
        return "Rendelés hozzáadva!"

    def fizetes(self, asztal_szam, vasarlo_neve, kiszolgalo_neve):
        asztal = self.asztalok[asztal_szam - 1]
        if not asztal.nyitva:
            return "Az asztalnál nincs aktív rendelés."

        osszeg, tetelek = asztal.lezaras()

        tetel_statisztika = {}
        for etel in tetelek:
            tetel_statisztika[etel] = tetel_statisztika.get(etel, 0) + 1

        tetel_string = ", ".join([f"{k} ({v}x)" for k, v in tetel_statisztika.items()])

        with open('vasarlasok.csv', 'a', encoding='utf-8', newline='') as f:
            iro = csv.writer(f, delimiter=';')
            iro.writerow([vasarlo_neve, kiszolgalo_neve, osszeg, tetel_string])

        return f"Fizetve: {osszeg} Ft. Köszönjük!"
