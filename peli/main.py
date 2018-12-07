import time, copy, json
import haravasto, miinakentta
tulokset = []
def luo_kentta(korkeus, leveys):
    lista = []
    for i in range(korkeus):
        lista.append([])
        for j in range(leveys):
            lista[i].append(" ")
    return lista
def tallenna_tulokset(tiedosto, tulokset):
    with open(tiedosto, "a") as lahde:
        lahde.write("Pelaaja: {}, Aika: {}, Miinojen määrä: {}, Kentan koko: {}x{} \n".format(tulokset["nimi"],
                                                                                        tulokset["aika"],
                                                                                        tulokset["miinojen_maara"],
                                                                                        tulokset["leveys"],
                                                                                        tulokset["korkeus"]
        ))
def lue_tulokset(tiedosto):
    with open(tiedosto) as lahde:
        rivit = lahde.readlines()
        for rivi in rivit:
            print(rivi)
def laske_kulunut_aika():
    return miinakentta.tila["lopetus"] - miinakentta.tila["aloitus"]
def muotoile_aika():
    aika = miinakentta.tila["aika"]
    aika // 60

def muotoile_tulokset(tulos_lista):
    for tulos in tulos_lista:
        print("Nimi: {}, Aika: {}, Miinojen määrä: {}, Kentta: {}x{}, 1: {}".format(tulos["nimi"],
                                                                                         tulos["aika"],
                                                                                         tulos["miinojen_maara"],
                                                                                         tulos["leveys"],
                                                                                         tulos["korkeus"],
                                                                                         tulos["tila"]))
def main():
    haravasto.lataa_kuvat("../spritet")
    miinakentta.tila["kentta_kopio"] = copy.deepcopy(miinakentta.tila["kentta"])
    miinakentta.tayta_kopio()
    miinakentta.aseta_kentan_korkeus_leveys()
    haravasto.luo_ikkuna((miinakentta.tila["kentan_leveys"] + 1) * 40,
                         (miinakentta.tila["kentan_korkeus"] + 1) * 40)
    miinakentta.miinoita(miinakentta.tila["kentta"],
                         miinakentta.laske_vapaat_ruudut(),
                         miinakentta.tila["miinojen_lkm"])
    miinakentta.sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(miinakentta.piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(miinakentta.hiiri_kasittelija)
    miinakentta.nollaa_tilat()
    miinakentta.tila["aloitus"] = time.perf_counter()
    haravasto.aloita()
if __name__ == "__main__":
    while True:
        print("Komennot: Aloita, Tulokset, Lopeta")
        komento = input("Anna komento: ").lower()
        if komento == "aloita":
            while True:
                try:
                    korkeus = int(input("Anna kentan korkeus kokonaislukuna: "))
                    leveys = int(input("Anna kentan leveys kokonaislukuna: "))
                    miinojen_lkm = int(input("Anna miinojen määrä: "))
                except ValueError:
                    print("Anna kokonaisluku!")
                else:
                    miinakentta.tila["kentta"] = luo_kentta(korkeus, leveys)
                    for k, rivi in enumerate(miinakentta.tila["kentta"]):
                        miinakentta.tila["miinojen_lkm"] = miinojen_lkm
                    main()
                    nimi = input("Anna pelaajan nimi: ")
                    pelaaja = {
                                "nimi": nimi,
                                "aika": miinakentta.tila["aika"],
                                "miinojen_maara": miinojen_lkm,
                                "leveys": leveys,
                                "korkeus": korkeus,
                                "tila": None
                                }
                    if miinakentta.tila["voitto"]:
                        pelaaja["tila"] = "Voitto"
                    else:
                        pelaaja["tila"] = "Tappio"
                    tallenna_tulokset("tulokset.txt", pelaaja)
                    break
        elif komento == "tulokset":
            try:
                tallennetut_tiedot = lue_tulokset("tulokset.txt")
            except FileNotFoundError:
                print("Tuloksia ei vielä ole.")
        elif komento == "lopeta":
            print("Hei hei!")
            break
        else:
            print("Komentoa ei ole olemassa")
