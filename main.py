import random

class Plateau:
    def __init__(self, colonne, ligne):
        self.c = colonne
        self.l = ligne
        self.plateau = []

    def creation_plateau(self):
        for i in range(self.l):
            ligne = []
            for j in range(self.c):
                ligne.append('0')
            self.plateau.append(ligne)

    def affichage_plateau(self):
        for ligne in self.plateau:
            for elem in ligne:
                print(elem.ljust(3), end='')
            print()

    def placer_mine(self):
        posx = random.randint(0,self.l-1)
        posy = random.randint(0, self.c-1)
        self.plateau[posx][posy] = 'B'


p = Plateau(5, 5)
p.creation_plateau()
for i in range(5):
    p.placer_mine()
#print(plateau)
p.affichage_plateau()