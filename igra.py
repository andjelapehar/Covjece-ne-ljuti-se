from .painter import ObojiPlocu
from collections import namedtuple, deque
import random

Pijun = namedtuple("Pijun", "index boja id")


        

class Igrac():
    
    def __init__(self, boja, ime=None, izaberi_pijun_delegate=None):
       
        self.boja = boja
        self.izaberi_pijun_delegate = izaberi_pijun_delegate
        self.ime = ime
        self.finished = False
        
     
        self.pijuni = [Pijun(i, boja, boja[0].upper() + str(i))
                      for i in range(1, 5)]

    def __str__(self):
        return "{}({})".format(self.ime, self.boja)

    def izaberi_pijun(self, pijuni):
        
        if len(pijuni) == 1:
            index = 0
        elif len(pijuni) > 1:
            if self.izaberi_pijun_delegate is None:
                index = random.randint(0, len(pijuni) - 1)
            else:
                index = self.izaberi_pijun_delegate()
        return index


class Ploca():
    


    PLOCA_VELICINA = 56

    
    PLOCA_BOJA_VELICINA = 7

    BOJA_POREDAK = ['zuta', 'plava', 'crvena', 'zelena']

    
    BOJA_UDALJENOST = 14

    def __init__(self):
        
        Ploca.BOJA_START = {
            boja: 1 + index * Ploca.BOJA_UDALJENOST for
            index, boja in enumerate(Ploca.BOJA_POREDAK)}
        
        Ploca.BOJA_END = {
            boja: index * Ploca.BOJA_UDALJENOST
            for index, boja in enumerate(Ploca.BOJA_POREDAK)}
        Ploca.BOJA_END['zuta'] = Ploca.PLOCA_VELICINA

        self.pijuni_possiotion = {}

        
        self.painter = ObojiPlocu()

       
        self.ploca_pool_pozicija = (0, 0)

    def postavi_pijun(self, pijun, pozicija):
       
        self.pijuni_possiotion[pijun] = pozicija

    def stavi_pijun_na_ploca_pool(self, pijun):
        self.postavi_pijun(pijun, self.ploca_pool_pozicija)

    def jeli_pijun_na_ploca_pool(self, pijun):
        
        return self.pijuni_possiotion[pijun] == self.ploca_pool_pozicija

    def stavi_pijun_na_pocetno_polje(self, pijun):
        start = Ploca.BOJA_START[pijun.boja.lower()]
        pozicija = (start, 0)
        self.postavi_pijun(pijun, pozicija)

    def mogucnost_pijun_kretanja(self, pijun, dobivena_vrijednost):
       
        common_poss, private_poss = self.pijuni_possiotion[pijun]
        if private_poss + dobivena_vrijednost > self.PLOCA_BOJA_VELICINA:
            return False
        return True

    def pomakni_pijun(self, pijun, dobivena_vrijednost):
       
        common_poss, private_poss = self.pijuni_possiotion[pijun]
        end = self.BOJA_END[pijun.boja.lower()]
        if private_poss > 0:
           
            private_poss += dobivena_vrijednost
        elif common_poss <= end and common_poss + dobivena_vrijednost > end:
           
            private_poss += dobivena_vrijednost - (end - common_poss)
            common_poss = end
        else:
        
            common_poss += dobivena_vrijednost
            if common_poss > self.PLOCA_VELICINA:
                common_poss = common_poss - self.PLOCA_VELICINA
        pozicija = common_poss, private_poss
        self.postavi_pijun(pijun, pozicija)

    def pijun_na_kraju(self, pijun):
       
        common_poss, private_poss = self.pijuni_possiotion[pijun]
        if private_poss == self.PLOCA_BOJA_VELICINA:
            return True
        return False

    def pijuni_ista_pozicija(self, pijun):
       
        pozicija = self.pijuni_possiotion[pijun]
        return [curr_pijun for curr_pijun, curr_postion in
                self.pijuni_possiotion.items()
                if pozicija == curr_postion]

    def paint_ploca(self):
        
        pozicije = {}
        for pijun, pozicija in self.pijuni_possiotion.items():
            common, private = pozicija
            if not private == Ploca.PLOCA_BOJA_VELICINA:
                pozicije.setdefault(pozicija, []).append(pijun)
        return self.painter.paint(pozicije)


class Kocka():

    MIN = 1
    MAX = 6

    @staticmethod
    def bacanje():
        return random.randint(Kocka.MIN, Kocka.MAX)


class Igra():
  

    def __init__(self):
        self.igraci = deque()
        self.mjesto = []
        self.ploca = Ploca()
      
        self.finished = False
       
        self.dobivena_vrijednost = None
     
        self.curr_igrac = None
       
        self.dopusten_pijuni = []
       
        self.izabran_pijun = None
     
        self.index = None
     
        self.jog_pijuni = []

    def dodaj_igrac(self, igrac):
        self.igraci.append(igrac)
        for pijun in igrac.pijuni:
            self.ploca.stavi_pijun_na_ploca_pool(pijun)

    def dostupne_boje(self):
       
        used = [igrac.boja for igrac in self.igraci]
        available = set(self.ploca.BOJA_POREDAK) - set(used)
        return sorted(available)

    def iduce_bacanje(self):
       
        if not self.dobivena_vrijednost == Kocka.MAX:
            self.igraci.rotate(-1)
        return self.igraci[0]

    def dohvati_pijun(self, igrac):
        
        for pijun in igrac.pijuni:
            if self.ploca.jeli_pijun_na_ploca_pool(pijun):
                return pijun

    def dohvati_dopustene_pijune_kretanje(self, igrac, dobivena_vrijednost):
        
        dopusten_pijuni = []
        if dobivena_vrijednost == Kocka.MAX:
            pijun = self.dohvati_pijun(igrac)
            if pijun:
                dopusten_pijuni.append(pijun)
        for pijun in igrac.pijuni:
            if not self.ploca.jeli_pijun_na_ploca_pool(pijun) and\
                    self.ploca.mogucnost_pijun_kretanja(pijun, dobivena_vrijednost):
                dopusten_pijuni.append(pijun)
        return sorted(dopusten_pijuni, key=lambda pijun: pijun.index)

    def dohvati_ploca_pic(self):
        return self.ploca.paint_ploca()

    def strani_pijun(self, pijun):
        pijuni = self.ploca.pijuni_ista_pozicija(pijun)
        for p in pijuni:
            if p.boja != pijun.boja:
                self.ploca.stavi_pijun_na_ploca_pool(p)
                self.jog_pijuni.append(p)

    def napravi_korak(self, igrac, pijun):
       
        if self.dobivena_vrijednost == Kocka.MAX and\
                self.ploca.jeli_pijun_na_ploca_pool(pijun):
            self.ploca.stavi_pijun_na_pocetno_polje(pijun)
            self.strani_pijun(pijun)
            return
        self.ploca.pomakni_pijun(pijun, self.dobivena_vrijednost)
        if self.ploca.pijun_na_kraju(pijun):
            igrac.pijuni.remove(pijun)
            if not igrac.pijuni:
                self.mjesto.append(igrac)
                self.igraci.remove(igrac)
                if len(self.igraci) == 1:
                    self.mjesto.extend(self.igraci)
                    self.finished = True
        else:
            self.strani_pijun(pijun)

    def pokreni_bacanje(self, ind=None, dobivena_v=None):
       
        self.jog_pijuni = []
        self.curr_igrac = self.iduce_bacanje()
        if dobivena_v is None:
            self.dobivena_vrijednost = Kocka.bacanje()
        else:
            self.dobivena_vrijednost = dobivena_v
        self.dopusten_pijuni = self.dohvati_dopustene_pijune_kretanje(
            self.curr_igrac, self.dobivena_vrijednost)
        if self.dopusten_pijuni:
            if ind is None:
                self.index = self.curr_igrac.izaberi_pijun(
                    self.dopusten_pijuni)
            else:
                self.index = ind
            self.izabran_pijun = self.dopusten_pijuni[self.index]
            self.napravi_korak(self.curr_igrac, self.izabran_pijun)
        else:
            self.index = -1
            self.izabran_pijun = None

