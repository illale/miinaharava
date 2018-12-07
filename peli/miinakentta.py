import random, copy, time
import haravasto
peli = {
    "kentta": None,
    "leveys": 0,
    "korkeus": 0,
    "kopio": None,
    "miinojen_lkm": 0,
    "häviö": False,
    "voitto": False,
    "aloitus": 0,
    "lopetus": 0,
    "aika": 0,
    "liike": True
}
def nollaa_tilat():
    peli["aloitus"] = 0
    peli["lopeuts"] = 0
    peli["häviö"] = False
    peli["voitto"] = False
    peli["aika"] = 0,
    peli["liike"] = True
def aseta_kentan_korkeus_leveys():
    peli["korkeus"] = len(peli["kentta"])
    peli["leveys"] = len(peli["kentta"][0])
def tarkista_listan_x(x, i, lista, rivi):
    if 0 < x < peli["leveys"] - 1:
        for j in range(-1, 2):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
    elif x == 0:
        for j in range(0, 2):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
    elif x == peli["leveys"] - 1:
        for j in range(-1, 1):
            if rivi[x + j] == " ":
                lista.append((x + j, i))
def tarkista_ruudut(lista, x, y):
    for i, rivi in enumerate(peli["kopio"]):
        if y == 0:
            if i < 2:
                tarkista_listan_x(x, i, lista, rivi)
        elif 0 < y < peli["korkeus"] - 1:
            if (y - 1) <= i <= (y + 1):
                tarkista_listan_x(x, i, lista, rivi)
        elif y == peli["korkeus"] - 1:
            if i > peli["korkeus"] - 3:
                tarkista_listan_x(x, i, lista, rivi)
def tulvataytto(x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    if peli["kentta"][y][x] == "x":
        pass
    else:
        koordinaatit = [(x, y)]
        while koordinaatit:
            alkio_x, alkio_y = koordinaatit.pop(-1)
            if peli["kentta"][alkio_y][alkio_x] == "0":
                peli["kopio"][alkio_y][alkio_x] = peli["kentta"][alkio_y][alkio_x]
                tarkista_ruudut(koordinaatit, alkio_x, alkio_y)
            elif peli["kentta"][alkio_y][alkio_x] == "x":
                pass
            elif peli["kentta"][alkio_y][alkio_x] != "0":
                peli["kopio"][alkio_y][alkio_x] = peli["kentta"][alkio_y][alkio_x]
def laske_vapaat_ruudut():
    """
    Laskee kentässa olevien vapaiden ruutujen määrän.
    """
    vapaat_ruudut = []
    for i, x_rivi in enumerate(peli["kentta"]):
        for j in range(len(x_rivi)):
                vapaat_ruudut.append((j, i))
    return vapaat_ruudut
def tayta_kopio():
    """
    Täyttää kopion " " merkillä.
    """
    for rivi in peli["kopio"]:
        for elementti in rivi:
            elementti = " "
def miinoita(vapaat_ruudut, miinojen_lkm):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinojen_lkm):
        miinoitettava_ruutu = random.randint(0, len(vapaat_ruudut))
        try:
            x_index, y_index = vapaat_ruudut[miinoitettava_ruutu]
            peli["kentta"][y_index][x_index] = "x"
            del vapaat_ruudut[miinoitettava_ruutu]
        except IndexError:
            pass
def lisaa_alkio_listaan(x, rivi, miina_lista):
    """
    Lisää koordinaattien vieressä olevat miinat listaan.
    """
    if 0 < x < peli["leveys"] - 1:
        for j in range(-1, 2):
            miina_lista.append(rivi[x + j])
    elif x == 0:
        for j in range(0, 2):
            miina_lista.append(rivi[x + j])
    elif x == peli["leveys"] - 1:
        for j in range(-1, 1):
            miina_lista.append(rivi[x + j])
def laske_vierekkaiset_miinat(x, y):
    """
    Laskee ruudun vieressä olevien miinojen määrä.
    """
    viereiset_ruudut = []
    for i, kentan_rivi in enumerate(peli["kentta"]):
        if y == 0:
            if i < 2:
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
        elif 0 < y < peli["korkeus"]:
            if (y - 1) <= i <= (y + 1):
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
        elif y == peli["korkeus"]:
            if i > peli["korkeus"] - 2:
                lisaa_alkio_listaan(x, kentan_rivi, viereiset_ruudut)
    miinojen_maara = viereiset_ruudut.count("x")
    return miinojen_maara
def sijoita_ruutu_kenttaan():
    """
    Määrittää minkalainen ruutu kentan jossain kohdassa pitää olla, ja sijoittaa
    sen siihen.
    """
    for i, rivi in enumerate(peli["kentta"]):
        for j, alkio in enumerate(rivi):
            if alkio == "x":
                pass
            elif alkio == " ":
                miinat = laske_vierekkaiset_miinat(j, i)
                if miinat == 0:
                    peli["kentta"][i][j] = "0"
                elif miinat != 0:
                    peli["kentta"][i][j] = str(miinat)
def laske_kulunut_aika():
    peli["aika"] = peli["lopetus"] - peli["aloitus"]
def hanki_ruudun_indeksi(x, y):
    """
    Palauttaa oikeat indeksit listaa varten koordinaattien perusteella.
    """
    for i in range(peli["korkeus"]):
        if i * 40 < y < (i + 1) * 40:
            for j in range(peli["leveys"]):
                if j * 40 < x < (j + 1) * 40:
                    palautettava_i = peli["korkeus"] - (i + 1)
                    return (j, palautettava_i)
def paljasta_miinat():
    for i, rivi in enumerate(peli["kentta"]):
        for j, alkio in enumerate(rivi):
            if peli["kentta"][i][j] == "x":
                peli["kopio"][i][j] = peli["kentta"][i][j]
def laske_miinojen_maara_kopiossa():
    lista = []
    for rivi in peli["kopio"]:
        for alkio in rivi:
            if alkio == "x":
                lista.append(1)
    maara = lista.count(1)
    if maara == peli["miinojen_lkm"]:
        return False
    elif maara != peli["miinojen_lkm"]:
        return True
def laske_suljetut_ruudut():
    suljettujen_maara = 0
    for rivi in peli["kopio"]:
        suljettujen_maara += rivi.count(" ")
        suljettujen_maara += rivi.count("f")
    return suljettujen_maara
def tarkista_voitto():
    lista = []
    for i, rivi in enumerate(peli["kopio"]):
        for j in range(len(rivi)):
            kopion_alkio = peli["kopio"][i][j]
            kentan_alkio = peli["kentta"][i][j]
            if (kopion_alkio == "f" or kopion_alkio == " ") and kentan_alkio == "x" :
                lista.append(1)
    maara = lista.count(1)
    sul = laske_suljetut_ruudut()
    if maara == peli["miinojen_lkm"] and 0 <= sul <= maara:
        peli["voitto"] = True
def hiiri_kasittelija(x, y, painike, muokkausnappaimet):
    if peli["liike"]:
        if painike == haravasto.HIIRI_VASEN:
            try:
                j, i = hanki_ruudun_indeksi(x, y)
            except TypeError:
                pass
            else:
                elementti = peli["kentta"][i][j]
                if elementti == "x":
                    paljasta_miinat()
                    peli["häviö"] = True
                else:
                    peli["kopio"][i][j] = elementti
                    tulvataytto(j, i)
                    tarkista_voitto()
        elif painike == haravasto.HIIRI_OIKEA:
            try:
                j, i = hanki_ruudun_indeksi(x, y)
            except TypeError:
                pass
            else:
                if peli ["kopio"][i][j] == " ":
                    peli["kopio"][i][j] = "f"
                elif peli["kopio"][i][j] == "f":
                    peli["kopio"][i][j] = " "
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
    for i, lista in enumerate(peli["kopio"]):
        for j, alkio in enumerate(lista):
            y_koordinaatti = (len(peli["kopio"]) - (i + 1)) * 40
            haravasto.lisaa_piirrettava_ruutu(alkio, j * 40, y_koordinaatti)
    haravasto.piirra_ruudut()
    if peli["häviö"]:
        peli["liike"] = False
        haravasto.piirra_tekstia("Hävisit, poistu painamalla ESC", 50,
                                 (peli["korkeus"] // 2) * 40 + 5, koko=20, vari=(244,66,66,255))
        peli["lopetus"] = time.perf_counter()
        laske_kulunut_aika()
    elif peli["voitto"]:
        peli["liike"] = False
        haravasto.piirra_tekstia("Voitit, poistu painamalla ESC", 50,
                                 (peli["korkeus"] // 2) * 40, koko=20, vari=(244,66,66,255))
        peli["lopetus"] = time.perf_counter()
        laske_kulunut_aika()
def main():
    haravasto.lataa_kuvat("../spritet")
    peli["kopio"] = copy.deepcopy(peli["kentta"])
    tayta_kopio()
    aseta_kentan_korkeus_leveys()
    haravasto.luo_ikkuna((peli["leveys"]) * 40, (peli["korkeus"]) * 40, taustavari=(0, 0, 0, 0))
    vapaat_ruudut = laske_vapaat_ruudut()
    miinoita(vapaat_ruudut, peli["miinojen_lkm"])
    sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    nollaa_tilat()
    for rivi in peli["kentta"]:
        print(rivi)
    haravasto.aloita()

if __name__ == "__main__":
    peli["kentta"] = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
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
    peli["miinojen_lkm"] = 20
    main()
