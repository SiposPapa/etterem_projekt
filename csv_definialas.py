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

