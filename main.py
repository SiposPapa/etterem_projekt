
# Ez a program egy étterem egyszerű menürendszere.
# A felhasználó tud rendelést felvenni, fizetést intézni,
# és meg tudja nézni a raktárkészletet.
# A rendelések feldolgozását az EtteremRendszer osztály végzi,
# amit a menurendszer.py fájlban kell megírni.

from menurendszer import EtteremRendszer


def beolvas_egesz_szam(prompt):
    """
    Ez egy nagyon egyszerű segédfüggvény.
    Célja: a felhasználótól kérünk egy számot, de nem használunk try-exceptet.
    A felhasználó bármit beírhat, például betűket vagy üres stringet.
    Ilyenkor None értéket ad vissza, amiből tudjuk, hogy nem számot kaptunk.

    Működés:
    - bekérjük a bemenetet
    - levágjuk a szüneteket (strip)
    - megnézzük, hogy szám-e (lstrip('-') megengedi a negatív előjelet is)
    - ha igen: visszaadjuk int() formában
    - ha nem: kiírjuk, hogy hiba van, és None visszatérítés

    A program többi részében mindig ellenőrizzük, hogy a visszatérési érték None-e.
    """
    szoveg = input(prompt).strip()

    # Ha a felhasználó számot adott meg (negatív is lehet), akkor int-té alakítjuk
    if szoveg.lstrip('-').isdigit():
        return int(szoveg)

    # Ha nem szám, akkor hibát jelzünk
    print("Érvénytelen bevitel: egész számot kell megadni.")
    return None


def main():
    print("Üdv az étteremben!")

    # Itt kérjük be, hány asztal legyen.
    # Érvénytelen bemenet esetén kilépünk.
    asztalok_szama = beolvas_egesz_szam("Hány asztallal indul az egység? ")

    # Ha nem számot adott meg a felhasználó
    if asztalok_szama is None:
        print("Kilépés: nem adott meg érvényes számot.")
        return

    # A szám nem lehet kisebb mint 1
    if asztalok_szama < 1:
        print("Legalább 1 asztal szükséges. Kilépés.")
        return

    # Létrehozzuk az éttermi rendszert a megadott asztalszámmal
    rendszer = EtteremRendszer(asztalok_szama)

    # A fő menü ciklus, ami addig fut, amíg ki nem lépünk belőle.
    while True:
        print("\n1. Új tétel rendelése")
        print("2. Fizetés / Asztal lezárása")
        print("3. Raktárkészlet megtekintése")
        print("4. Kilépés")

        # Menu választás
        valasztas = input("Válasszon opciót: ")
        valasztas.strip()


        # 1. Új rendelés felvétele
        if valasztas == "1":
            # Asztalszám bekérése
            asztal = beolvas_egesz_szam("Asztal száma: ")

            if asztal is None:
                # Rossz bevitel esetén a fenti függvény már kiírt hibát.
                continue

            if asztal < 1:
                print("Az asztalszám legalább 1 kell legyen.")
                continue

            # Étel neve
            etel = input("Étel neve: ").strip()
            if not etel:
                print("Kérjük, adjon meg egy ételnevet.")
                continue

            # Meghívjuk a rendszer rendelésfelvételét
            eredmeny = rendszer.rendeles_felvetel(asztal, etel)
            print(eredmeny)

        # 2. Fizetés / Asztal lezárása
        elif valasztas == "2":
            # Asztal száma
            asztal = beolvas_egesz_szam("Melyik asztal fizet? ")

            if asztal is None:
                continue

            if asztal < 1:
                print("Az asztalszám legalább 1 kell legyen.")
                continue

            # Vevő neve
            vevo = input("Vevő neve: ").strip()
            # Felszolgáló neve
            felszolga = input("Felszolgáló neve: ").strip()

            # Meghívjuk a fizetés logikáját
            eredmeny = rendszer.fizetes(asztal, vevo, felszolga)
            print(eredmeny)

        # ------------------------------
        # 3. Raktárkészlet
        # ------------------------------
        elif valasztas == "3":
            # Közvetlenül elérjük a raktar attribútumot
            # Feltételezzük, hogy létezik és dict típusú.
            if not rendszer.raktar:
                print("A raktár üres vagy nincs feltöltve.")
            else:
                print("\nRaktárkészlet:")
                # Kiírjuk szépen sorban a készletet
                for alapanyag, mennyiseg in sorted(rendszer.raktar.items()):
                    print(f"{alapanyag}: {mennyiseg}")

        # ------------------------------
        # 4. Kilépés
        # ------------------------------
        elif valasztas == "4":
            print("Viszlát!")
            break

        # ------------------------------
        # Hibás menüpont
        # ------------------------------
        else:
            print("Ismeretlen opció, próbálja újra.")


# Ha közvetlenül futtatjuk a fájlt, akkor induljon el a main()
if __name__ == "__main__":
    main()
``


