from objects import Object
from globals import *
from colors import colors

class Obstacle(Object):

    def __init__(self):
        y = GRID['WIDTH']
        x = randint(GRID['GROUND'], GRID['ROOF']-1)
        super().__init__(x,y)

class Coin(Obstacle):
    def __init__(self):
        super().__init__()
        self._design = coin
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x + i , self._y + j):
                    mp.matrix[mp.height - self._x + i ][self._y + j] = ' '

    def update_matrix(self):
        if not self._visible:
            self.shift()
            return
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        count = 0
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x + i, self._y + j):
                    coll = check_collision(mp.height - self._x + i,self._y + j)
                    if coll is "Safe":
                        mp.matrix[mp.height - self._x + i ][self._y + j] = 'C'
                    else :
                        if coll is "Mando":
                            count +=1
        if count > 0:
            self.remove()
            return 1
    
    def render(self,choice):
        self.rrender(colors.fg.yellow,1,1,0,0,choice)
    
class Laser(Obstacle):
    def __init__(self):
        super().__init__()
        self._orientation = randint(0,2)
        self._xoff = LASER['ORIENTATION'][self._orientation][0]
        self._yoff = LASER['ORIENTATION'][self._orientation][1]
        self._design = laser[self._orientation]
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        self.render(' ')
        mp = self._matrix
        xoff , yoff = self._xoff,self._yoff

        for i in range(LASER['LENGTH']):
                if in_border(mp.height-self._x - 4 - i*xoff,self._y - i*yoff):
                    if mp.matrix[mp.height-self._x - 4 - i*xoff][self._y - i*yoff] == 'L':
                        mp.matrix[mp.height-self._x - 4 - i*xoff][self._y - i*yoff] = ' '

    def update_matrix(self):
        if not self._visible:
            self.shift()
            return
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        xoff , yoff = self._xoff,self._yoff
        for i in range(LASER['LENGTH']):
            if in_border(mp.height-self._x - 4 - i*xoff,self._y - i*yoff):
                coll = check_collision(mp.height-self._x - 4 - i*xoff,self._y - i*yoff)
                if coll is "Safe":
                    mp.matrix[mp.height-self._x - 4 - i*xoff][self._y - i*yoff] = 'L'
                else :
                    self.remove()
                    if coll is "Bullet":
                        return "Bullet"
                    return "Mando"
    
    def render(self,choice):
        xoff , yoff = self._xoff,self._yoff
        for i in range(self.height()):
                if in_border(mp.height-self._x - 4 - i*xoff,self._y - i*yoff):
                    pprint(self,colors.fg.red,mp.height-self._x - 4 - i*xoff,self._y - i*yoff,self._design[self.height()-1-i][0] if choice is 'Y' else ' ')

class Speedup(Obstacle):
    def __init__(self):
        super().__init__()
        self._design = speed
        self.setheight()
        self.setwidth()

    def erase_matrix(self):
        mp = self._matrix
        self.render(' ')
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x + i , self._y + j):
                    mp.matrix[mp.height - self._x + i ][self._y + j] = ' '

    def update_matrix(self):
        if not self._visible:
            self.shift()
            return
        self.erase_matrix()
        self.shift()
        self.render('Y')
        mp = self._matrix
        for i in range(self.height()):
            for j in range(self.width()):
                if in_border(mp.height - self._x + i, self._y + j):
                    coll = check_collision(mp.height - self._x + i,self._y + j)
                    if coll is "Safe":
                        mp.matrix[mp.height - self._x ][self._y] = 'P'
                    else :
                        if coll is "Mando":
                            self.remove()
                            return True

    def render(self,choice):
        self.rrender(colors.fg.yellow,1,1,0,0,choice)