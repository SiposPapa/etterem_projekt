# Parancssori menü a rendszerhez.
# Fapados bevitelkezelés: ha nem számot kapunk, jelezzük és visszalépünk a menübe.
# Opciók:
# 1. Rendelés felvétele (azonnali raktárcsökkentéssel)
# 2. Fizetés / asztal lezárása (és vásárlás mentése)
# 3. Raktárkészlet megtekintése
# 4. Kilépés
# 5. Új étel felvétele az étlapra (NÉV, ÁR, RECEPT)
# 6. Étel törlése az étlapról

from menurendszer import EtteremRendszer


def beolvas_egesz_szam(szoveg):
    be = input(szoveg).strip()
    if be.lstrip('-').isdigit():
        return int(be)
    print("Érvénytelen bevitel: egész számot kell megadni.")
    return None


def beolvas_float(szoveg):
    # Float-beolvasás: csak pontot lehet tizedesnek.
    be = input(szoveg).strip().replace(',', '.')
    # egész is lehet (pl. "2")
    if be.replace('.', '', 1).lstrip('-').isdigit():
        try:
            return float(be)
        except:
            pass
    print("Érvénytelen bevitel: számot kell megadni (pl. 1 vagy 1.5).")
    return None


def main():
    print("Üdv az étteremben!")

    asztalok_szama = beolvas_egesz_szam("Hány asztallal indul az egység? ")
    if asztalok_szama is None:
        print("Kilépés: nem adott meg érvényes számot.")
        return
    if asztalok_szama < 1:
        print("Legalább 1 asztal szükséges. Kilépés.")
        return

    rendszer = EtteremRendszer(asztalok_szama)

    while True:
        print("\n1. Új tétel rendelése")
        print("2. Fizetés / Asztal lezárása")
        print("3. Raktárkészlet megtekintése")
        print("4. Kilépés")
        print("5. Új étel felvétele az étlapra")
        print("6. Étel törlése az étlapról")

        valasztas = input("Válasszon opciót: ").strip()

        # 1) Új rendelés felvétele
        if valasztas == "1":
            asztal = beolvas_egesz_szam("Asztal száma: ")
            if asztal is None or asztal < 1:
                print("Az asztalszám legalább 1 kell legyen.")
                continue

            etel = input("Étel neve: ").strip()
            if not etel:
                print("Kérjük, adjon meg egy ételnevet.")
                continue

            print(rendszer.rendeles_felvetel(asztal, etel))

        # 2) Fizetés
        elif valasztas == "2":
            asztal = beolvas_egesz_szam("Melyik asztal fizet? ")
            if asztal is None or asztal < 1:
                print("Az asztalszám legalább 1 kell legyen.")
                continue

            vevo = input("Vevő neve: ").strip()
            felszolga = input("Felszolgáló neve: ").strip()
            print(rendszer.fizetes(asztal, vevo, felszolga))

        # 3) Raktárkészlet
        elif valasztas == "3":
            if not rendszer.raktar:
                print("A raktár üres vagy nincs feltöltve.")
            else:
                print("\nRaktárkészlet:")
                for alapanyag in sorted(rendszer.raktar.keys()):
                    print(alapanyag + ": " + str(rendszer.raktar[alapanyag]))

        # 4) Kilépés
        elif valasztas == "4":
            print("Viszlát!")
            break

        # 5) Új étel felvétele az étlapra
        elif valasztas == "5":
            nev = input("Új étel neve: ").strip()
            if not nev:
                print("Hibás név.")
                continue
            ar = beolvas_egesz_szam("Ár (Ft): ")
            if ar is None or ar < 0:
                print("Hibás ár.")
                continue

            # Recept felvétel: megkérdezzük, hány alapanyagot ad meg
            alap_db = beolvas_egesz_szam("Hány alapanyagot vesz fel a recepthez? ")
            if alap_db is None or alap_db < 0:
                print("Hibás darabszám.")
                continue

            hozzavalok = {}
            i = 1
            while i <= alap_db:
                alap = input("Alapanyag neve #" + str(i) + ": ").strip()
                if not alap:
                    print("Hibás név.")
                    break
                menny = beolvas_float("Szükséges mennyiség #" + str(i) + " (pl. 0.2): ")
                if menny is None or menny < 0:
                    print("Hibás mennyiség.")
                    break
                hozzavalok[alap] = menny
                i += 1

            if len(hozzavalok) != alap_db:
                print("Recept felvétele megszakítva.")
                continue

            print(rendszer.etel_hozzaad(nev, ar, hozzavalok))

        # 6) Étel törlése az étlapról
        elif valasztas == "6":
            nev = input("Melyik ételt töröljük az étlapról? ").strip()
            if not nev:
                print("Hibás név.")
                continue
            print(rendszer.etel_torles(nev))

        else:
            print("Ismeretlen opció, próbálja újra.")


if __name__ == "__main__":
    main()

