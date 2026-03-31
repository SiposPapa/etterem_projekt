from menurendszer import EtteremRendszer
 
def main():
    print("Üdv az étteremben! ")
    asztalok_szama = int(input("Hány asztallal indul az egység? "))
    rendszer = EtteremRendszer(asztalok_szama)
 
    while True:
        print("\n1. Új tétel rendelése")
        print("2. Fizetés / Asztal lezárása")
        print("3. Raktárkészlet megtekintése")
        print("4. Kilépés")
        valasztas = input("Válasszon opciót: ")
 
        if valasztas == "1":
            aszk = int(input("Asztal száma: "))
            etel = input("Étel neve: ")
            print(rendszer.rendeles_felvetel(aszk, etel))
        elif valasztas == "2":
            aszk = int(input("Melyik asztal fizet? "))
            v_nev = input("Vevő neve: ")
            f_nev = input("Felszolgáló neve: ")
            print(rendszer.fizetes(aszk, v_nev, f_nev))
 
        elif valasztas == "3":
            # Listázás tétele
            for alap, menny in rendszer.raktar.items():
                print(f"{alap}: {menny}")
 
        elif valasztas == "4":
            break
 
if __name__ == "__main__":
    main()
