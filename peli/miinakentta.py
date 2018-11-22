import random, copy
import haravasto
tila = {
    "kentta": None,
    "kentan_leveys": 0,
    "kentan_korkeus": 0,
    "kentta_kopio": None,
    "lista": []
}
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
            print(koordinaatit)
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
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    for i in range(miinojen_lkm + 1):
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
def hanki_ruudun_indeksi(x, y):
    """
    Palauttaa oikeat indeksit listaa varten koordinaattien perustteella.
    """
    for i in range(tila["kentan_korkeus"] + 1):
        if i * 40 < y < (i + 1) * 40:
            for j in range(tila["kentan_leveys"] + 1):
                if j * 40 < x < (j + 1) * 40:
                    palautettava_i = len(tila["kentta"]) - (i + 1)
                    return (j, palautettava_i)
def hiiri_kasittelija(x, y, painike, muokkausnappaimet):
    if painike == haravasto.HIIRI_VASEN:
        try:
            alkio_x, alkio_y = hanki_ruudun_indeksi(x, y)
        except TypeError:
            pass
        else:
            print(alkio_x, alkio_y)
            elementti = tila["kentta"][alkio_y][alkio_x]
            tila["kentta_kopio"][alkio_y][alkio_x] = elementti
            tulvataytto(alkio_x, alkio_y)

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
def main():
    haravasto.lataa_kuvat("../spritet")
    vapaat_ruudut = laske_vapaat_ruudut()
    miinoita(tila["kentta"], vapaat_ruudut, 20)
    sijoita_ruutu_kenttaan()
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
    for i, rivi in enumerate(tila["kentta"]):
        print(tila["kentta"][i])
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
    tila["kentta_kopio"] = copy.deepcopy(tila["kentta"])
    tayta_kopio()
    tila["kentan_korkeus"] = len(tila["kentta"]) - 1
    tila["kentan_leveys"] = len(tila["kentta"][0]) - 1
    haravasto.luo_ikkuna((tila["kentan_leveys"] + 1) * 40, (tila["kentan_korkeus"] + 1) * 40)
    main()
