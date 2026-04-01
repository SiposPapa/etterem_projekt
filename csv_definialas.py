
# Etel: név, ár, recept (alapanyag -> mennyiség)
# Asztal: rendelések listája, összegszámítás, lezárás.

class Etel:
    def __init__(self, nev, ar, receptek):
        # nev: string
        # ar: int vagy float
        # receptek: dict (kulcs: alapanyag neve, érték: mennyiség float)
        self.nev = nev
        self.ar = ar
        self.receptek = receptek


class Asztal:
    def __init__(self, szam):
        self.szam = szam
        self.rendelesek = []   # Etel objektumok listája
        self.nyitva = False    # lesz True, ha van rendelés

    def hozzaad(self, etel):
        # Etel objektumot ad hozzá a rendelésekhez.
        self.rendelesek.append(etel)
        self.nyitva = True

    def osszeg_szamitas(self):
        # Összegzés tétele: végigmegyünk és összeadjuk az árakat.
        osszesen = 0
        for etel in self.rendelesek:
            osszesen += etel.ar
        return osszesen

    def lezaras(self):
        # Lezáráskor:
        # - kiszámoljuk az összeget
        # - kigyűjtjük a rendelt ételek neveit (klasszikus for ciklus)
        # - visszaállítjuk az asztalt alaphelyzetbe
        osszeg = self.osszeg_szamitas()

        nevek_listaja = []
        for etel in self.rendelesek:
            nevek_listaja.append(etel.nev)

        self.rendelesek = []
        self.nyitva = False

        return osszeg, nevek_listaja

# Etel: név, ár, recept (alapanyag -> mennyiség)
# Asztal: rendelések listája, összegszámítás, lezárás.

class Etel:
    def __init__(self, nev, ar, receptek):
        # nev: string
        # ar: int vagy float
        # receptek: dict (kulcs: alapanyag neve, érték: mennyiség float)
        self.nev = nev
        self.ar = ar
        self.receptek = receptek


class Asztal:
    def __init__(self, szam):
        self.szam = szam
        self.rendelesek = []   # Etel objektumok listája
        self.nyitva = False    # lesz True, ha van rendelés

    def hozzaad(self, etel):
        # Etel objektumot ad hozzá a rendelésekhez.
        self.rendelesek.append(etel)
        self.nyitva = True

    def osszeg_szamitas(self):
        # Összegzés tétele: végigmegyünk és összeadjuk az árakat.
        osszesen = 0
        for etel in self.rendelesek:
            osszesen += etel.ar
        return osszesen

    def lezaras(self):
        # Lezáráskor:
        # - kiszámoljuk az összeget
        # - kigyűjtjük a rendelt ételek neveit (klasszikus for ciklus)
        # - visszaállítjuk az asztalt alaphelyzetbe
        osszeg = self.osszeg_szamitas()

        nevek_listaja = []
        for etel in self.rendelesek:
            nevek_listaja.append(etel.nev)

        self.rendelesek = []
        self.nyitva = False

        return osszeg, nevek_listaja

# Etel: név, ár, recept (alapanyag -> mennyiség)
# Asztal: rendelések listája, összegszámítás, lezárás.

class Etel:
    def __init__(self, nev, ar, receptek):
        # nev: string
        # ar: int vagy float
        # receptek: dict (kulcs: alapanyag neve, érték: mennyiség float)
        self.nev = nev
        self.ar = ar
        self.receptek = receptek


class Asztal:
    def __init__(self, szam):
        self.szam = szam
        self.rendelesek = []   # Etel objektumok listája
        self.nyitva = False    # lesz True, ha van rendelés

    def hozzaad(self, etel):
        # Etel objektumot ad hozzá a rendelésekhez.
        self.rendelesek.append(etel)
        self.nyitva = True

    def osszeg_szamitas(self):
        # Összegzés tétele: végigmegyünk és összeadjuk az árakat.
        osszesen = 0
        for etel in self.rendelesek:
            osszesen += etel.ar
        return osszesen

    def lezaras(self):
        # Lezáráskor:
        # - kiszámoljuk az összeget
        # - kigyűjtjük a rendelt ételek neveit (klasszikus for ciklus)
        # - visszaállítjuk az asztalt alaphelyzetbe
        osszeg = self.osszeg_szamitas()

        nevek_listaja = []
        for etel in self.rendelesek:
            nevek_listaja.append(etel.nev)

        self.rendelesek = []
        self.nyitva = False

        return osszeg, nevek_listaja
