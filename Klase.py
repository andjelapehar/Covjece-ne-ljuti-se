from random import randint

class Igrac:

    def __init__(self, b, igrac_id): 
        self.igrac_id = igrac_id
        self.figure = [Figura(igrac_id, i, b) for i in range(4)]


    def play(self, bacanja):
        for bacanje in bacanja:
            figura = self.figure[randint(0,3)] 
            if figura.in_prison():
                if bacanje == 6:
                    figura.move(1)
            else:
                figura.move(1)
                     
    def get_igac_id(self):
        return self.igrac_id
    
    
class Korak:
    
    
    def __init__(self, val=None):
        self.val = val
        self.next = None
    
    def look_forward(self, n):
        if n <= 0:
            return True
        elif not self.next:
            return False
        
        return self.next.look_forward(n-1)
    
    def putanja(self):
        p = []
        s = self
        while s:
            p.append(s)
            s = s.next
        return p
        
    def __repr__(self):
        return self.val.__repr__()
    

	
class Figura:


    def __init__(self, osoba_id, figura_id, b):
        self.osoba_id = osoba_id
        self.figura_id = figura_id
        self.ploca = b
        self.path = self.generate_path(b.igrac_count)
		
    def generate_path(self, igrac_count):
        i = 2 + self.osoba_id * 13
        step = Step(self.ploca.ploca[0][self.osoba_id][self.figura_id])
        step.val.contents = self
        start = step
        
        j = 2
        while j < (player_count) * 13:
            step.next = Step(self.ploca.ploca[1][i])
            step = step.next
            j += 1
            i = (i + 1) % ((igrac_count) * 13)
            
        j = 0
        while j < 5:
            step.next = Step(self.ploca.ploca[2][self.osoba_id][j])
            step = step.next
            j += 1
        return start
        
    def in_prison(self):
        return self.path.val == self.ploca.ploca[0][self.osoba_id][self.figura_id]
        
    def move(self, steps):
        start = self.path
        piece = self.path.val
        if self.path.look_forward(steps):
            for i in range(steps):
                self.path = self.path.next
        start.val.contents = self.__repr__()
        self.path.val.contents = piece
        
    def __repr__(self):
        return "({};{})".format(self.osoba_id, self.figura_id)

    def __repr__1(self):
        return "'no'"



