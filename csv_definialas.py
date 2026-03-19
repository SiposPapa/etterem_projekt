class Etel:
    def __init__(self, nev, ar, receptek):
        self.nev = nev
        self.ar = ar
        self.receptek = receptek  #Dictionary: pl: "etel": "pizza", mert szebb, mint a lista, pl: "etel":"3"

class Asztal:
    def __init__(self, szam):
        self.szam = szam   #Itt tároljuk az Etel objektumokat
        self.rendelesek = []    #Követi, hogy ki mit rendelt az adott asztalnál
        self.nyitva = False

    def hozzaad(self, etel): #Egy Etel objektumot ad, és az asztala True lesz
            self.rendelesek.append(etel)
            self.nyitva = True
 
    def osszeg_szamitas(self):
        # Összegzés tétele
        osszesen = 0
        for etel in self.rendelesek:
            osszesen += etel.ar
        return osszesen
    def lezaras(self):
        #Összegszámítás, függvény meghívás
        osszeg = self.osszeg_szamitas()
        # Listakészítés            
        nevek_listaja = []
        for etel in self.rendelesek:
            nevek_listaja.append(etel.nev)
        #Adatok alaphelyzetbe állítása, asztal nyitása
        self.rendelesek = []
        self.nyitva = False
        return osszeg, nevek_listaja
