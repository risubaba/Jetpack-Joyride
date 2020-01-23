from objects import Person
from globals import *
import numpy as np

class Player(Person):

    def __init__(self, x, y):
        super().__init__(x, y)
        self._ltime = time()
        self._lives = 3
        self._score = 0
        self._shield = False
        self._ondragon = False
        self.update_matrix()
        self._magnetattr = time()
        self._design = mando
        self.setheight()
        self.setwidth()

    def health(self):
        return GAME['LIVES']

    def ondragon(self):
        return self._ondragon

    def protected(self):
        return GAME['SHIELD']

    def shieldon(self):
        GAME['SHIELD'] = True
        self.setdesign()

    def shieldoff(self):
        self.erase_matrix()
        GAME['SHIELD'] = False
        self.setdesign()

    def death(self):
        if self._ondragon is True:
            self._ondragon = False
            return

        if not self.protected():
            GAME['LIVES'] = GAME['LIVES'] - 1

    def setdesign(self):
        if self._ondragon:
            self._design = wiggly
        elif self.protected():
            self._design = protectedmando
        else:
            self._design = mando
        self.setheight()
        self.setwidth()
        
    def rrender(self,color,x,y,xx,yy,choice):
        if self._ondragon:
            for i in range(self.height()):
                for j in range(self.width()):
                    if in_border(mp.height-self._x + i*x + xx[j], self._y + j*y+yy):
                            pprint(self,color,mp.height-self._x + i*x + xx[j], self._y + j*y+yy,self._design[self.height()-1-i][j] if choice is 'Y' else ' ')
        else:
            for i in range(self.height()):
                for j in range(self.width()):
                    if in_border(mp.height-self._x + i*x + xx, self._y + j*y+yy):
                            pprint(self,color,mp.height-self._x + i*x + xx, self._y + j*y+yy,self._design[self.height()-1-i][j] if choice is 'Y' else ' ')
            
    

    def score(self):
        return self._score

    def scoreup(self):
        self._score = self.score() + 1

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        xoff , yoff = (-1,-1) if self.protected() else (0,0)
        for i in range(xoff,self.height()-xoff):
            for j in range(yoff,self.width()+2-yoff):
                mp.matrix[mp.height-self._x-i][self._y+j] = ' '

    def update_matrix(self):
        self.gravity()
        self.render('Y')
        mp = self._matrix
        xoff , yoff = (-1,-1) if self.protected() else (0,0)
        for i in range(self.height()):
            for j in range(self.width() + 2):
                mp.matrix[mp.height-self._x-i][self._y+j] = 'M'

        for i in range(xoff,self.height()-xoff):
            for j in range(yoff,self.width() + 2 -yoff):
                if mp.matrix[mp.height-self._x-i][self._y+j] == ' ':
                    mp.matrix[mp.height-self._x-i][self._y+j] = 'S'

    def render(self,choice):
        if self._ondragon:
            from time import sleep
            arr = np.concatenate([ 2*(np.sin(ll(time()*8//4,8,1))) for i in range(24//24)])
            brr = [ [i,i,i] for i in arr ]
            arr = np.concatenate([ i for i in brr])
            arr = np.concatenate([arr,[arr[-1] for i in range(14)]])
            self.rrender(colors.bold+colors.fg.blue,-1,1,arr,0,choice)
        else:
            self.rrender(colors.bold+colors.fg.blue,-1,1,0,0,choice)

    def mdown(self):
        displacement = min(10,max(0,(2*self._airtime) - 1)) # min to mimic terminal velocity :)
        self._x = max(PLAYER['BOTTOMBORDER'] + (3 if self._ondragon else 0) ,self._x-displacement)
        if self._x <= GRID['GROUND'] + 1:
            self._airtime = 0
        self._airtime = self._airtime + 1

    def mup(self):
        self._airtime = 0
        self._x = min(PLAYER['TOPBORDER'] - 3, self._x+2*GAME['SPEED'])
    def execute(self, key):
        self.erase_matrix()
        if key is "d":
            self.mright(3)

        if key is "a":
            self.mleft(3)

        if key is "w":
            self.mup()
        
        if key is "aa":
            if time() - self._magnetattr > 0.75:
                self._magnetattr = time()
                self.mleft(3)
        
        if key is "dd":
            if time() - self._magnetattr > 0.75:
                self._magnetattr = time()
                self.mright(3)

        if key is "f":
            self._ondragon = True

        self.update_matrix()

        if key is "e" and not self._ondragon:
            return True
        return False

class Boss(Person):
    def __init__(self,x,y):
        super().__init__(x,y)
        self._design = dragon 
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        mp = self._matrix
        self.render(' ')
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x - i , self._y + j):
                    mp.matrix[mp.height - self._x - i ][self._y + j] = ' '

    def update_matrix(self):
        self.gravity()
        if not self._visible:
            return
        mp = self._matrix
        self.render('Y')

        collide = False
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x - i , self._y + j):
                    if j is 0:
                        coll = check_collision(mp.height - self._x - i , self._y - 1*GAME['SPEED'])
                        if coll is not "Safe":
                            mp.matrix[mp.height - self._x - i][self._y + j] = '-'
                            collide =  True
                    else :
                        mp.matrix[mp.height - self._x - i][self._y + j] = '-'
        return collide

    def mup(self):
        self._airtime = 0
        self._x = min(PLAYER['TOPBORDER'] -self.height(), self._x+2*GAME['SPEED'])

    def update(self,player):
        self.erase_matrix()
        if player.xcoord() > self.xcoord():
            self.mup()
        if self.update_matrix():
            return True
    
    def render(self,choice):
        self.rrender(colors.fg.orange,-1,1,0,0,choice)
