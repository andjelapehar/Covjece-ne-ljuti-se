from .igra import Igrac, Igra
from .painter import kocka_6
from os import linesep


class Prikaz():

    def __init__(self):
        self.prompt_end = "> "
        self.igra = Igra()
 
        self.prompted_for_pijun = False
       
     
    def prikaziPocetakIgre():
        print("*" *50)
        print("*" *20+ " ČOVJEČE NE LJUTI SE " + "*"*20)
        print("*" *50)
    def provjera_unosa(self, prompt, desire_type, dopusten_unos=None,
                       poruka_greske="Nevaljan unos!", duljina_stringa=None):
        
       
        prompt += linesep + self.prompt_end
        while True:
            izbor = input(prompt)
            if not izbor:
                print(linesep + poruka_greske)
                continue
            try:
                izbor = desire_type(izbor)
            except ValueError:
                print(linesep + poruka_greske)
                continue
            if dopusten_unos:
                if izbor in dopusten_unos:
                    break
                else:
                    print("Nevaljan unos!")
                    continue
            elif duljina_stringa:
                min_duljina, max_duljina = duljina_stringa
                if min_duljina < len(izbor) < max_duljina:
                    break
                else:
                    print(linesep + poruka_greske)
            else:
                break
        print()
        return izbor

    def dohvati_korisnikov_pocetni_izbor(self):
        text = linesep.join(["izaberi opciju:",
                             "0 - Izađi iz igre",
                             "1 - Pokreni novu igru"
                            ])
        izbor = self.provjera_unosa(text, int, (0, 1))
        return izbor
    

    


    def upit_za_igraca(self):

        dostupne_boje = self.igra.dostupne_boje()
        text = linesep.join(["izaberi tip igraca",
                             "0 - računalo",
                             "1 - čovjek"])
        izbor = self.provjera_unosa(text, int, (0, 1))

        if izbor == 1:
            ime = self.provjera_unosa("Unesite ime za igrača: ",
                                       str, duljina_stringa=(1, 30))
            dostupne_opcije = range(len(dostupne_boje))
            if len(dostupne_opcije) > 1:
                opcije = ["{} - {}".format(index, boja)
                           for index, boja in
                           zip(dostupne_opcije,
                           dostupne_boje)]
                text = "Izaberite boju:" + linesep
                text += linesep.join(opcije)
                izbor = self.provjera_unosa(text, int, dostupne_opcije)
                boja = dostupne_boje.pop(izbor)
            else:
                boja = dostupne_boje.pop()
            igrac = Igrac(boja, ime, self.prompt_izaberi_pijun)
        elif izbor == 0:
            boja = dostupne_boje.pop()
            igrac = Igrac(boja)
        self.igra.dodaj_igrac(igrac)

    def prompt_za_igraci(self):

        counts = ("prvog", "drugog", "treceg", "cetvrtog")
        dodavanje_text = "Dodaj {} igraca"
        for i in range(4):
            print(dodavanje_text.format(counts[i]))
            self.upit_za_igraca()
            print("Igrac dodan")
       

        

    def prompt_izaberi_pijun(self):

        text = kocka_6(self.igra.dobivena_vrijednost,
                                  str(self.igra.curr_igrac))
        text += linesep + " ima više od jednog pijuna za micanje."
        text += " Izaberi pijun" + linesep
        pijun_opcije = ["{} - {}".format(index + 1, pijun.id)
                        for index, pijun
                        in enumerate(self.igra.dopusten_pijuni)]
        text += linesep.join(pijun_opcije)
        index = self.provjera_unosa(
            text, int, range(1, len(self.igra.dopusten_pijuni) + 1))
        self.prompted_for_pijun = True
        return index - 1

    def prompt_za_nastavak(self):
        text = "Pritisni enter za nastavak" + linesep
        input(text)

    def print_igraci_info(self):
        word = "start" if self.igra.dobivena_vrijednost is None else "nastavi"
        print("igra {} s {} igraci:".format(
              word,
              len(self.igra.igraci)))
        for igrac in self.igra.igraci:
            print(igrac)
        print()

    def print_info_poslije_micanja(self):
        pijuni_id = [pijun.id for pijun in self.igra.dopusten_pijuni]
        poruka = kocka_6(self.igra.dobivena_vrijednost,
                                     str(self.igra.curr_igrac))
        poruka += linesep
        if self.igra.dopusten_pijuni:
            poruka_o_premještanju = "{} je pomaknut. ".format(
                self.igra.izabran_pijun.id)
            if self.prompted_for_pijun:
                self.prompted_for_pijun = False
                print(poruka_o_premještanju)
                return
            poruka += "{} mogući pijuni za micanje.".format(
                " ".join(pijuni_id))
            poruka += " " + poruka_o_premještanju
            if self.igra.jog_pijuni:
                poruka += "Pomakni pijun "
                poruka += " ".join([pijun.id for pijun in self.igra.jog_pijuni])
        else:
            poruka += "Nijedan pijun se ne može pomaknuti."
        print(poruka)

    def print_mjesto(self):
        mjesto_list = ["{} - {}".format(index + 1, igrac)
                         for index, igrac in enumerate(self.igra.mjesto)]
        poruka = "Mjesto:" + linesep + linesep.join(mjesto_list)
        print(poruka)

    def print_ploca(self):
        print(self.igra.dohvati_ploca_pic())



    def ucitaj_igrace_za_novu_igru(self):
        self.prompt_za_igraci()
        self.print_igraci_info()

    def play_igra(self):
       
        try:
            while not self.igra.finished:
                self.igra.pokreni_bacanje()
                self.print_info_poslije_micanja()
                self.print_ploca()

                self.prompt_za_nastavak()
            print("Igra završena")
            self.print_mjesto()
        except (KeyboardInterrupt, EOFError):
            print(linesep +
                  "Napuštanje igre. ")
            raise
    def start(self):
        print()
        try:
            izbor = self.dohvati_korisnikov_pocetni_izbor()
            if izbor == 0:  
                quit()
            elif izbor == 1:
                self.ucitaj_igrace_za_novu_igru()
                self.play_igra()
                
       
        except (KeyboardInterrupt, EOFError):
            print(linesep + "Exit igra")

Prikaz.prikaziPocetakIgre()
if __name__ == '__main__':
    Prikaz().start()
