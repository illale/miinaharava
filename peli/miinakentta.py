import random, copy, time
import haravasto
tila = {
    "kentta": None,
    "kentan_leveys": 0,
    "kentan_korkeus": 0,
    "kentta_kopio": None,
    "miinojen_lkm": 0,
    "häviö": False,
    "voitto": False,
    "aloitus": 0,
    "lopetus": 0,
    "aika": 0
}
def nollaa_tilat():
    tila["aloitus"] = 0
    tila["lopeuts"] = 0
    tila["häviö"] = False
    tila["voitto"] = False
    tila["aika"] = 0
def aseta_kentan_korkeus_leveys():
    tila["kentan_korkeus"] = len(tila["kentta"]) - 1
    tila["kentan_leveys"] = len(tila["kentta"][0]) - 1
def tarkista_listan_x(x, i, lista, rivi, leveys):
    if 0 < x < leveys:
        for j in range(-1, 2):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
    elif x == 0:
        for j in range(0, 2):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
    elif x == leveys:
        for j in range(-1, 1):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
def tarkista_ruudut(kentta, lista, x, y):
    p_korkeus = len(kentta) - 1
    p_leveys = len(kentta[0]) - 1
    for i, rivi in enumerate(kentta):
        if y == 0:
            while i < 2:
                tarkista_listan_x(x, i, lista, rivi, p_leveys)
                break
        elif 0 < y < p_korkeus:
            while (y - 1) <= i <= (y + 1):
                tarkista_listan_x(x, i, lista, rivi, p_leveys)
                break
        elif y == p_korkeus:
            while i > p_korkeus - 2:
                tarkista_listan_x(x, i, lista, rivi, p_leveys)
                break
def tulvataytto(x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    if tila["kentta"][y][x] == "x":
        pass
    else:
        koordinaatit = [(x, y)]
        while koordinaatit:
            alkio_x, alkio_y = koordinaatit.pop(-1)
            if tila["kentta"][alkio_y][alkio_x] == "0":
                tila["kentta_kopio"][alkio_y][alkio_x] = tila["kentta"][alkio_y][alkio_x]
                tarkista_ruudut(tila["kentta_kopio"], koordinaatit, alkio_x, alkio_y)
            elif tila["kentta"][alkio_y][alkio_x] == "x":
                pass
            elif tila["kentta"][alkio_y][alkio_x] != "0":
                tila["kentta_kopio"][alkio_y][alkio_x] = tila["kentta"][alkio_y][alkio_x]
def laske_vapaat_ruudut():
    """
    Laskee kentässa olevien vapaiden ruutujen määrän.
    """
    vapaat_ruudut = []
    for i, x_rivi in enumerate(tila["kentta"]):
        for j, alkio in enumerate(x_rivi):
                vapaat_ruudut.append((j, i))
    return vapaat_ruudut
def tayta_kopio():
    """
    Täyttää kopion " " merkillä.
    """
    for i, rivi in enumerate(tila["kentta_kopio"]):
        for j, elementti in enumerate(rivi):
            elementti = " "
def miinoita(miinakentta, vapaat_ruudut, miinojen_lkm):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinojen_lkm):
        miinoitettava_ruutu = random.randint(0, len(vapaat_ruudut))
        try:
            x_index, y_index = vapaat_ruudut[miinoitettava_ruutu]
            miinakentta[y_index][x_index] = "x"
            del vapaat_ruudut[miinoitettava_ruutu]
        except IndexError:
            pass
def lisaa_alkio_listaan(x, rivi, miina_lista):
    """
    Lisää koordinaattien vieressä olevat miinat listaan.
    """
    if 0 < x < tila["kentan_leveys"]:
        for j in range(-1, 2):
            miina_lista.append(rivi[x + j])
    elif x == 0:
        for j in range(0, 2):
            miina_lista.append(rivi[x + j])
    elif x == tila["kentan_leveys"]:
        for j in range(-1, 1):
            miina_lista.append(rivi[x + j])
def laske_vierekkaiset_miinat(x, y, miinakentta):
    """
    Laskee ruudun vieressä olevien miinojen määrä.
    """
    viereiset_ruudut = []
    for i, kentan_rivi in enumerate(miinakentta):
        if y == 0:
            if i < 2:
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
        elif 0 < y < tila["kentan_korkeus"]:
            if (y - 1) <= i <= (y + 1):
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
        elif y == tila["kentan_korkeus"]:
            if i > tila["kentan_korkeus"] - 2:
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
    miinojen_maara = viereiset_ruudut.count("x")
    return miinojen_maara
def sijoita_ruutu_kenttaan():
    """
    Määrittää minkalainen ruutu kentan kohdassa pitää olla, ja sijoittaa
    sen siihen.
    """
    for i, rivi in enumerate(tila["kentta"]):
        for j, alkio in enumerate(rivi):
            if tila["kentta"][i][j] == "x":
                pass
            elif tila["kentta"][i][j] == " ":
                miinat = laske_vierekkaiset_miinat(j, i, tila["kentta"])
                if miinat == 0:
                    tila["kentta"][i][j] = "0"
                elif miinat != 0:
                    tila["kentta"][i][j] = str(miinat)
def laske_kulunut_aika():
    tila["aika"] = tila["lopetus"] - tila["aloitus"]
def hanki_ruudun_indeksi(x, y):
    """
    Palauttaa oikeat indeksit listaa varten koordinaattien perusteella.
    """
    for i in range(tila["kentan_korkeus"] + 1):
        if i * 40 < y < (i + 1) * 40:
            for j in range(tila["kentan_leveys"] + 1):
                if j * 40 < x < (j + 1) * 40:
                    palautettava_i = len(tila["kentta"]) - (i + 1)
                    return (j, palautettava_i)
def paljasta_miinat():
    for i, rivi in enumerate(tila["kentta"]):
        for j, alkio in enumerate(rivi):
            if tila["kentta"][i][j] == "x":
                tila["kentta_kopio"][i][j] = tila["kentta"][i][j]
def laske_miinojen_maara_kopiossa():
    lista = []
    for i, rivi in enumerate(tila["kentta_kopio"]):
        for j, alkio in enumerate(rivi):
            if tila["kentta_kopio"][i][j] == "x":
                lista.append(1)
    maara = lista.count(1)
    if maara == tila["miinojen_lkm"]:
        return False
    elif maara != tila["miinojen_lkm"]:
        return True
def laske_suljetut_ruudut():
    suljettujen_maara = 0
    for rivi in tila["kentta_kopio"]:
        suljettujen_maara += rivi.count(" ")
    return suljettujen_maara
def tarkista_voitto():
    lista = []
    for i, rivi in enumerate(tila["kentta_kopio"]):
        for j in range(len(rivi)):
            kopion_elementti = tila["kentta_kopio"][i][j]
            kentan_elementti = tila["kentta"][i][j]
            if (kopion_elementti == "f" or kopion_elementti == " ") and kentan_elementti == "x" :
                lista.append(1)
    maara = lista.count(1)
    if maara == tila["miinojen_lkm"] and laske_suljetut_ruudut() == maara:
        tila["voitto"] = True
def hiiri_kasittelija(x, y, painike, muokkausnappaimet):
    if laske_miinojen_maara_kopiossa():
        if painike == haravasto.HIIRI_VASEN:
            try:
                alkio_x, alkio_y = hanki_ruudun_indeksi(x, y)
            except TypeError:
                pass
            else:
                elementti = tila["kentta"][alkio_y][alkio_x]
                if elementti == "x":
                    paljasta_miinat()
                    tila["häviö"] = True
                else:
                    tila["kentta_kopio"][alkio_y][alkio_x] = elementti
                    tulvataytto(alkio_x, alkio_y)
                    tarkista_voitto()
        elif painike == haravasto.HIIRI_OIKEA:
            try:
                alkio_x, alkio_y = hanki_ruudun_indeksi(x, y)
            except TypeError:
                pass
            else:
                if tila ["kentta_kopio"][alkio_y][alkio_x] == " ":
                    tila["kentta_kopio"][alkio_y][alkio_x] = "f"
                elif tila["kentta_kopio"][alkio_y][alkio_x] == "f":
                    tila["kentta_kopio"][alkio_y][alkio_x] = " "
                tarkista_voitto()
def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for i, lista in enumerate(tila["kentta_kopio"]):
        for j, alkio in enumerate(lista):
            y_koordinaatti = (len(tila["kentta_kopio"]) - (i + 1)) * 40
            haravasto.lisaa_piirrettava_ruutu(alkio, j * 40, y_koordinaatti)
    haravasto.piirra_ruudut()
    if tila["häviö"]:
        haravasto.muuta_ikkunan_koko((tila["kentan_leveys"] + 1) * 40, (tila["kentan_korkeus"] + 2) * 40)
        haravasto.piirra_tekstia("Hävisit, poistu painamalla ESC", 10,
                                 (tila["kentan_korkeus"] + 1) * 40 + 10, koko=20, vari=(255,0,255,100))
        tila["lopetus"] = time.perf_counter()
        laske_kulunut_aika()
    elif tila["voitto"]:
        haravasto.muuta_ikkunan_koko((tila["kentan_leveys"] + 1) * 40, (tila["kentan_korkeus"] + 2) * 40)
        haravasto.piirra_tekstia("Voitit, poistu painamalla ESC", 10,
                                 (tila["kentan_korkeus"] + 1) * 40 + 10, koko=20, vari=(255,0,255,100))
        tila["lopetus"] = time.perf_counter()
        laske_kulunut_aika()
def main():
    haravasto.lataa_kuvat("../spritet")
    tila["kentta_kopio"] = copy.deepcopy(tila["kentta"])
    tayta_kopio()
    tila["kentan_korkeus"] = len(tila["kentta"]) - 1
    tila["kentan_leveys"] = len(tila["kentta"][0]) - 1
    haravasto.luo_ikkuna((tila["kentan_leveys"] + 1) * 40, (tila["kentan_korkeus"] + 1) * 40)
    vapaat_ruudut = laske_vapaat_ruudut()
    miinoita(tila["kentta"], vapaat_ruudut, tila["miinojen_lkm"])
    sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    nollaa_tilat()
    for rivi in tila["kentta"]:
        print(rivi)
    haravasto.aloita()

if __name__ == "__main__":
    tila["kentta"] = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                      [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]
    tila["miinojen_lkm"] = 20
    main()
