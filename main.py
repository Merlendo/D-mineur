import random
import copy

class coordsErrorOutofrange(Exception):
    pass

class coordErrorMaskoff(Exception):
    pass


class Case:
    def __init__(self,bombe=False):
        self.bombe = bombe
        self.mask = True
        self.bombeadj = 0

    def unmask(self):
        if not self.mask:
            raise coordErrorMaskoff

        self.mask = False
        return self.bombe

    def affichage(self,DEBUG=False):
        if(self.mask and not DEBUG):
            print('*', end=" ")
        elif(self.bombe):
            print("B", end=" ")
        else: 
            print(self.bombeadj, end=" ")

class Plateau:
    
    def __init__(self, colonne, ligne, pourcentage):
        self.c = colonne
        self.l = ligne
        self.plateau = [[Case(random.randint(0,100) <= pourcentage) for j in range(self.c)] for i in range(self.l)]
        self.nbombe = 0

        for x in range(self.l):
            for y in range(self.c):
                if self.plateau[x][y].bombe:
                    self.nbombe += 1
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            if (x+dx >= 0 and x+dx < self.l) and (y+dy >= 0 and y+dy < self.c):
                                self.plateau[x+dx][y+dy].bombeadj += 1
                            

    def affichage(self,DEBUG=False):
        for ligne in self.plateau:
            for elem in ligne:
                elem.affichage(DEBUG)
            print()

    def creuser(self,l,c):
        if l > self.l or c > self.c:
            raise coordsErrorOutofrange()
        return self.plateau[l-1][c-1].unmask()

def coord(p):
    l = int(input("Ligne : "))
    c = int(input("Colonne : "))
    try : 
        return p.creuser(l,c)
    except coordsErrorOutofrange:
        print("Coordonnées Trop grande")
        return coord(p)
    except coordErrorMaskoff:
        print("Coordonnées déja rentrées")
        return coord(p)

        

p = Plateau(16,16, 10)
#print(plateau)
while True:
    p.affichage(True)
    print()
    p.affichage()
    if coord(p):
        print("Ta perdu")
        break
