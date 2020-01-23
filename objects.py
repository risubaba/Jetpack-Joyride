from globals import *
from colors import colors

class Object():
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._matrix = mp
        self._ctime = time()
        self._visible = True
        self._height = 0
        self._width = 0
        self._design = ''

    def xcoord(self):
        return self._x

    def ycoord(self):
        return self._y

    def Ctime(self):
        return self._ctime

    def height(self):
        return self._height

    def width(self):
        return self._width
        
    def mright(self, offset):
        self._y = self.ycoord()+offset*GAME['SPEED']

    def mleft(self, offset):
        self._y = self.ycoord()-offset*GAME['SPEED']

    def shift(self):
        if time() - self.Ctime() > 0.025:
            self.mleft(1)            
            self._ctime = time()

    def getdesign(self):
        return self._design
        
    def erase_matrix(self):
        pass

    def remove(self):
        self.erase_matrix()
        self._visible = False

    def rrender(self,color,x,y,xx,yy,choice):
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height-self._x + i*x + xx, self._y + j*y+yy):
                        pprint(self,color,mp.height-self._x + i*x + xx, self._y + j*y+yy,self._design[self.height()-1-i][j] if choice is 'Y' else ' ')

    def setheight(self):
        self._height = len(self.getdesign())
    
    def setwidth(self):
        self._width = len(self.getdesign()[0])


class Person(Object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self._airtime = 0

    def mright(self, offset):
        self._y = min(self.ycoord()+offset*GAME['SPEED'], PLAYER['RIGHTBORDER'] - 5)

    def mleft(self, offset):
        self._y = max(self.ycoord()-offset*GAME['SPEED'], PLAYER['LEFTBORDER'])

    def mdown(self):
        displacement = min(10,max(0,(2*self._airtime) - 1)) # min to mimic terminal velocity :)
        self._x = max(PLAYER['BOTTOMBORDER'],self._x-displacement)
        if self._x <= GRID['GROUND'] + 1:
            self._airtime = 0
        self._airtime = self._airtime + 1
    
    def gravity(self):
        if time() - self._ctime > 0.3:
            self.mdown()
            self._ctime = time()

class Bullet(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._design = bulletdesign
        self.setheight()
        self.setwidth()

    def shift(self):
        if time() - self._ctime > 0.03:
            self._y += 1*GAME['SPEED']
            self._ctime = time()

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        for i in range(BULLET['WIDTH']):
            if in_border(mp.height-self._x, self._y + i):
                mp.matrix[mp.height-self._x][self._y + i] = ' '

    def update_matrix(self):
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        for i in range(BULLET['WIDTH']):
            if in_border(mp.height-self._x, self._y + i):
                mp.matrix[mp.height-self._x][self._y + i] = 'B'
            
    def render(self,choice):
        self.rrender(colors.fg.lightgreen,0,1,0,0,choice)

class Snowball(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._design = snowball
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        for i in range(SNOWBALL['LENGTH']):
            for j in range(SNOWBALL['WIDTH']):
                if in_border(mp.height-self._x + i, self._y + j):
                    mp.matrix[mp.height-self._x + i][self._y + j] = ' '

    def update_matrix(self):
        if not self._visible:
            self.shift()
            return
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        for i in range(SNOWBALL['LENGTH']):
            for j in range(SNOWBALL['WIDTH']):
                if in_border(mp.height-self._x + i, self._y + j):
                    coll = check_collision(mp.height-self._x + i, self._y + j)
                    if coll is "Safe":
                        mp.matrix[mp.height-self._x + i][ self._y + j] = 'K'
                    else :
                        self.remove()
                        if coll is "Bullet":
                            return False
                        return True

    def render(self,choice):
        self.rrender('',1,1,0,0,choice)

class Magnet(Object):
    def __init__(self,x,y):
        super().__init__(x,y)
        self._design = magnet
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        for i in range(MAGNET['LENGTH']):
            for j in range(MAGNET['WIDTH']):
                if in_border(mp.height-self._x + j, self._y + i):
                    mp.matrix[mp.height-self._x + j][self._y + i] = ' '

    def update_matrix(self):
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        for i in range(MAGNET['LENGTH']):
            for j in range(MAGNET['WIDTH']):
                if in_border(mp.height-self._x + j, self._y + i):
                    mp.matrix[mp.height-self._x + j][self._y + i] = 'G'
        
    def render(self,choice):
        self.rrender(colors.fg.purple,1,1,0,0,choice)
    



