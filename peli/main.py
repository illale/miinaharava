import time, copy
import haravasto, miinakentta
def luo_kentta(korkeus, leveys):
    lista = []
    for i in range(korkeus):
        lista.append([])
        for j in range(leveys):
            lista[i].append(" ")
    return lista
def tallenna_tulokset(tiedosto):
    with open(tiedosto, -a) as lahde:
        lahde.write(tulokset)
def lue_tulokset(tiedosto):
    with open(tiedosto) as lahde:
        for rivi in lahde.readlines():
            print(rivi)
def laske_kulunut_aika():
    return miinakentta.tila["lopetus"] - miinakentta.tila["aloitus"]
def muotoile_aika(aika):
    pass
def main():
    haravasto.lataa_kuvat("../spritet")
    miinakentta.tila["kentta_kopio"] = copy.deepcopy(miinakentta.tila["kentta"])
    miinakentta.tayta_kopio()
    miinakentta.laske_kentan_korkeus_leveys()
    haravasto.luo_ikkuna((miinakentta.tila["kentan_korkeus"] + 1) * 40,
                         (miinakentta.tila["kentan_leveys"] + 2) * 40)
    miinakentta.miinoita(miinakentta.tila["kentta"],
                         miinakentta.laske_vapaat_ruudut(),
                         miinakentta.tila["miinojen_lkm"])
    miinakentta.sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(miinakentta.piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(miinakentta.hiiri_kasittelija)
    haravasto.aloita()
if __name__ == "__main__":
    print("Komennot: Aloita, Tulokset, lopeta")
    komento = input("Anna komento: ")
    komento.lower()
    if komento == "aloita":
        korkeus = int(input("Anna kentan korkeus: "))
        leveys = int(input("Anna kentan leveys: "))
        miinojen_lkm = int(input("Anna miinojen määrä: "))
        miinakentta.tila["kentta"] = luo_kentta(korkeus, leveys)
        for k, rivi in enumerate(miinakentta.tila["kentta"]):
            print(rivi)
        miinakentta.tila["miinojen_lkm"] = miinojen_lkm
        main()
    elif komento == "tulokset":
        pass
    elif komento == "lopeta":
        exit()
