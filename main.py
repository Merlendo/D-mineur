import random
import copy

class coordsErrorOutofrange(Exception):
    pass

class coordErrorMaskoff(Exception):
    pass

class coordErrorFlagon(Exception):
    pass

class ErrorToomanyFlag(Exception):
    pass
    
class Case:
    def __init__(self,bombe=False):
        self.bombe = bombe
        self.mask = True
        self.bombeadj = 0
        self.flag = False

    def flagon(self):
        if not self.mask:
            raise coordErrorMaskoff()
        
        self.flag = not self.flag
        
        return (self.flag, self.flag and self.bombe)

    def unmask(self):
        if not self.mask:
            raise coordErrorMaskoff
        if self.flag:
            raise coordErrorFlagon

        self.mask = False
        return self.bombe

    def affichage(self,DEBUG=False):
        if(self.flag and not DEBUG):
            print("@", end=" ")
        elif(self.mask and not DEBUG):
            print('*', end=" ")
        elif(self.bombe):
            print("#", end=" ")
        else: 
            print(self.bombeadj, end=" ")

class Plateau:
    
    def __init__(self, colonne, ligne, pourcentage):
        self.c = colonne
        self.l = ligne
        self.plateau = [[Case(random.randint(0,100) <= pourcentage) for j in range(self.c)] for i in range(self.l)]
        self.nbombe = 0
        self.nflag = 0
        self.flagonbombe = 0

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
        if self.plateau[l-1][c-1].bombeadj == 0:
            self.remplissage(l-1, c-1)
            return False
        else:
            return self.plateau[l-1][c-1].unmask()

    def remplissage(self, x, y):
        #condition : pas de bombes adjacentes + 0 < x < self.l + 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if ((x+dx >= 0 and x+dx < self.l) and (y+dy >= 0 and y+dy < self.c)) and self.plateau[x+dx][y+dy].mask:
                    self.plateau[x+dx][y+dy].mask = False
                    if self.plateau[x+dx][y+dy].bombeadj == 0:
                        self.remplissage(x+dx,y+dy)
    
    def poserdrapeau(self, l, c):
        #rajouté conditions nbombe + nflag and flags == bombes
        flagok, onbombe = self.plateau[l-1][c-1].flagon()
        
        if flagok:
            self.nflag += 1 
            if onbombe:
                self.flagonbombe += 1
        else:
            self.nflag -= 1
            if onbombe:
                self.flagonbombe -= 1
        
        if self.nflag > self.nbombe: 
            self.plateau[l-1][c-1].flagon()
            self.nflag -= 1
            if onbombe:
                self.flagonbombe -= 1
            raise ErrorToomanyFlag
        

class Jeu:
    def __init__(self):
        self.p = Plateau(5,5,10)
    
    def coord(self, fonction):
        l = int(input("Ligne : "))
        c = int(input("Colonne : "))
        try : 
            return fonction(self.p,l,c)
        except coordsErrorOutofrange:
            print("Coordonnées Trop grande")
            return coord(fonction)
        except coordErrorMaskoff:
            print("Coordonnées déja rentrées")
            return coord(fonction)
        except coordErrorFlagon:
            print("Drapeau posé, impossible de creuser")
            return coord(fonction)
        except ErrorToomanyFlag:
            print("Trop de drapeaux")
            return self.run()

    def run(self):
        while not self.victoire():

            self.p.affichage(True)
            print()
            self.p.affichage()
            
            action = "0"
            while action not in ["1","2"]:
                print("1 - CREUSER | 2 - POSER DRAPEAU")
                action = input("> ")
            if action == "1":
                if self.coord(Plateau.creuser):
                    print("Tu as Perdu...")
                    exit()
            else:
                self.coord(Plateau.poserdrapeau)
        print("Vous avez gagné !")

    def victoire(self):

        #Toutes les bombes on un drapeau
        victoire = False
        if self.p.flagonbombe == self.p.nbombe:
            victoire = True

        #Toutes les cases sont décochées:
        v = True
        for line in self.p.plateau:
            for elem in line:
                if elem.mask and not elem.bombe:
                    v = False

        return victoire or v

j = Jeu()
j.run()
