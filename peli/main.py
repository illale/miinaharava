import time, copy
import haravasto
import miinakentta as mk
def luo_kentta(korkeus, leveys):
    lista = []
    for i in range(korkeus):
        lista.append([])
        for j in range(leveys):
            lista[i].append(" ")
    return lista
def tallenna_tulokset(tiedosto, tulokset):
    with open(tiedosto, "a") as lahde:
        lahde.write("P: {}, A: {}, M: {}, Kk: {}x{}, Lt: {}, Vk: {}, Pvm: {} \n".format(tulokset["nimi"],
                                                                                        tulokset["aika"],
                                                                                        tulokset["miinojen_maara"],
                                                                                        tulokset["leveys"],
                                                                                        tulokset["korkeus"],
                                                                                        tulokset["tila"],
                                                                                        tulokset["vuorot"],
                                                                                        tulokset["päivä"]))
def lue_tulokset(tiedosto):
    with open(tiedosto) as lahde:
        rivit = lahde.readlines()
        for rivi in rivit:
            rivi.strip("\n")
            print(rivi)
def hanki_paivamaara():
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
def laske_kulunut_aika():
    return mk.peli["lopetus"] - mk.peli["aloitus"]
def muotoile_aika():
    aika = mk.peli["aika"]
    try:
        minuutit = int(aika // 60)
        sekunnit = round(aika % 60)
    except TypeError:
        minuutit = 0
        sekunnit = 0
    muotoilu = "{:02}:{:02}".format(minuutit, sekunnit)
    return muotoilu
def main():
    haravasto.lataa_kuvat("../spritet")
    mk.peli["kopio"] = copy.deepcopy(mk.peli["kentta"])
    mk.tayta_kopio()
    mk.aseta_kentan_korkeus_leveys()
    haravasto.luo_ikkuna((mk.peli["leveys"]) * 40,
                         (mk.peli["korkeus"] + 1) * 40)
    mk.miinoita(mk.laske_vapaat_ruudut(),
                mk.peli["miinojen_lkm"])
    mk.sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(mk.piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(mk.hiiri_kasittelija)
    mk.nollaa_tilat()
    mk.peli["aloitus"] = time.perf_counter()
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
                    mk.peli["kentta"] = luo_kentta(korkeus, leveys)
                    for k, rivi in enumerate(mk.peli["kentta"]):
                        mk.peli["miinojen_lkm"] = miinojen_lkm
                    main()
                    nimi = input("Anna pelaajan nimi: ")
                    aika = muotoile_aika()
                    pelaaja = {
                                "nimi": nimi,
                                "aika": aika,
                                "miinojen_maara": miinojen_lkm,
                                "leveys": leveys,
                                "korkeus": korkeus,
                                "tila": mk.peli["tila"],
                                "vuorot": mk.peli["siirtojen_maara"],
                                "päivä": hanki_paivamaara()
                                }
                    tallenna_tulokset("tulokset.txt", pelaaja)
                    break
        elif komento == "tulokset":
            try:
                print("P = Pelaaja, A = Aika, M = Miinojen määrä,")
                print("Kk = Kentän koko, Lt = Lopputulos, Vm = Vuorojen määrä,")
                print("Pvm = Päivämäärä")
                tallennetut_tiedot = lue_tulokset("tulokset.txt")
            except FileNotFoundError:
                print("Tuloksia ei ole vielä olemassa")
        elif komento == "lopeta":
            print("Hei hei!")
            break
        else:
            print("Komentoa ei ole olemassa")
