import random
import copy
import tkinter
from tkinter.font import Font

ACT_CREUSE = 1
ACT_FLAG = 2

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

    def affichage(self, fen, DEBUG=False):
        if(self.flag and not DEBUG):
            return fen.draw_flag
        elif(self.mask and not DEBUG):
            return fen.draw_dirt
        elif(self.bombe):
            return fen.draw_bombe
        else: 
            return lambda x, y : fen.draw_numero(self.bombeadj, x, y)

class Affichage():
    def __init__(self, lignes, collones):

        self.TAILLE_C = 25
        self.TAILLE_X = collones*self.TAILLE_C
        self.TAILLE_Y = lignes*self.TAILLE_C

        self.fen = tkinter.Tk()
        
        self.fen.title("D-mineur")
        self.fen.resizable(False, False)
        self.can = tkinter.Canvas(self.fen, bg='grey',height = self.TAILLE_Y, width = self.TAILLE_X)
        self.can.pack()
        self.can.bind("<Button-1>", self.creuser) 
        self.can.bind("<Button-3>", self.flagit) 
        
        self.dirtimg = tkinter.PhotoImage(file="IMG/dirt.gif")
        self.bombeimg = tkinter.PhotoImage(file="IMG/bombe2.gif")
        self.flagimg = tkinter.PhotoImage(file="IMG/flag.gif")
        self.retrofont = Font(family="Retro Gaming")
    def grille(self):
        for x in range(j.p.l):
            for y in range(j.p.c):
                self.can.create_rectangle(x*self.TAILLE_C, y*self.TAILLE_C, (x+1)*self.TAILLE_C , (y+1)*self.TAILLE_C, image=dirt)

    def draw_dirt(self, x, y):
        self.can.create_image(x*self.TAILLE_C,y*self.TAILLE_C, image=self.dirtimg, anchor="nw")
        #self.can.create_rectangle(x*self.TAILLE_C, y*self.TAILLE_C, (x+1)*self.TAILLE_C, (y+1)*self.TAILLE_C, fill="grey")

    def draw_bombe(self, x, y):
        self.can.create_image(x*self.TAILLE_C,y*self.TAILLE_C, image=self.bombeimg, anchor="nw")
        #self.can.create_rectangle(x*self.TAILLE_C, y*self.TAILLE_C, (x+1)*self.TAILLE_C, (y+1)*self.TAILLE_C, fill="red")
    
    def draw_flag(self, x, y):
        self.can.create_image(x*self.TAILLE_C,y*self.TAILLE_C, image=self.flagimg, anchor="nw")
        #self.can.create_rectangle(x*self.TAILLE_C, y*self.TAILLE_C, (x+1)*self.TAILLE_C, (y+1)*self.TAILLE_C, fill="green")

    def draw_numero(self, numero, x, y):
        if numero == 0:
            numero = " "
        if numero == 1:
            couleur = "blue"
        elif numero == 2:
            couleur = "green"
        elif numero == 3:
            couleur = "red"
        elif numero == 4:
            couleur = "purple"
        else:
            couleur = "black"
            
        self.can.create_rectangle(x*self.TAILLE_C, y*self.TAILLE_C, (x+1)*self.TAILLE_C, (y+1)*self.TAILLE_C, fill="#fdfcfd")
        self.can.create_text((self.TAILLE_C*(2*x+1))/2, (self.TAILLE_C*(2*y+1))/2, text=numero, fill=couleur, font=self.retrofont)

    def creuser(self, event):
        print("je clique position", event.x, event.y)
        j.run(ACT_CREUSE, int(event.x/self.TAILLE_C), int(event.y/self.TAILLE_C)) 
    
    def flagit(self, event):
        print("je clique droit position", event.x, event.y)
        j.run(ACT_FLAG, int(event.x/self.TAILLE_C), int(event.y/self.TAILLE_C)) 

    def end_line(self):
        pass

    def game_over(self):
        self.can.unbind("<Button-1>")
        self.can.unbind("<Button-3>")
        self.can.bind("<Button-1>",lambda event : j.new_game())


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
                            
    def affichage(self, fen, DEBUG=False):
        for y in range(self.l):
            for x in range(self.c):
                fonction = self.plateau[x][y].affichage(fen, DEBUG)
                fonction(x, y)
            fen.end_line()


    def creuser(self,l,c):
        if l > self.l-1 or c > self.c-1:
            raise coordsErrorOutofrange()
        if self.plateau[l][c].bombeadj == 0:
            self.plateau[l][c].unmask()
            self.remplissage(l, c)
            return False
        else:
            return self.plateau[l][c].unmask()

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
        flagok, onbombe = self.plateau[l][c].flagon()
        
        if flagok:
            self.nflag += 1 
            if onbombe:
                self.flagonbombe += 1
        else:
            self.nflag -= 1
            if onbombe:
                self.flagonbombe -= 1
        
        if self.nflag > self.nbombe: 
            self.plateau[l][c].flagon()
            self.nflag -= 1
            if onbombe:
                self.flagonbombe -= 1
            raise ErrorToomanyFlag
        

class Jeu:
    def __init__(self, x, y, pourcentage):
        self.x = x 
        self.y = y
        self.pourcentage = pourcentage
        self.p = Plateau(x,y,pourcentage)
        self.fen = Affichage(x,y)
        #self.fen_dbg = Affichage(x,y)
        #self.p.affichage(self.fen_dbg, True)
        
    def new_game(self):
        self.p = Plateau(self.x,self.y,self.pourcentage)
        self.fen.fen.destroy()
        self.fen = Affichage(x,y)
        self.run()
        
    def coord(self, fonction):
        l = int(input("Ligne : "))
        c = int(input("Colonne : "))
        try : 
            return fonction(self.p,l-1,c-1)
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

    def run_terminal(self):
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

    def run(self, action=None, x = None, y = None):
        self.fen.can.delete("all")
        try:
            if action == ACT_CREUSE:
                if self.p.creuser(x,y):
                    self.p.affichage(self.fen, True)
                    print("Tu as perdu !") 
                    self.fen.game_over()
                    self.fen.can.mainloop()
        
            elif action == ACT_FLAG:
                self.p.poserdrapeau(x,y)

            if self.victoire():
                self.p.affichage(self.fen, True)
                print("Tu as gagné !") 
                self.fen.game_over()
            else:    
                self.p.affichage(self.fen)
            
            self.fen.can.mainloop()

        except coordsErrorOutofrange:
            print("Coordonnées Trop grande")
            return self.run()
        except coordErrorMaskoff:
            print("Coordonnées déja rentrées")
            return self.run()
        except coordErrorFlagon:
            print("Drapeau posé, impossible de creuser")
            return self.run()
        except ErrorToomanyFlag:
            print("Trop de drapeaux")
            return self.run()

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

j = Jeu(32, 32, 10)
j.run()

