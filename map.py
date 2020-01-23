import numpy as np
import os
import random
from time import time
from globals import GRID , pos , GAME , gamestarttime , gametime , BULLET, BULLETS
from colors import colors

ground = GRID['GROUND']
height = GRID['HEIGHT']
width = GRID['WIDTH']


class map():
    
    def __init__(self):
        self.width = width
        self.height = height
        self.matrix = np.array([[' ' for i in range(width)] for j in range(height)])
        for i in range(3,5):
            self.matrix[i] = [ 'R' for j in range(width) ]
        for i in range(4):
            self.matrix[height - 4 + i] = [ 'G' for j in range(width)]

        self.shownmatrix = np.array([[' ' for i in range(width)] for j in range(height)])
        for i in range(3,6):
            self.shownmatrix[i] = [ 'R' for j in range(width) ]
        for i in range(4):
            self.shownmatrix[height - 5 + i] = [ 'G' for j in range(width)]

    def printmap(self):
        timeleft = int(gametime - ( time() - gamestarttime))
        score = "Score : " + str(GAME['SCORE'])
        lives = "|| Lives :" + str(GAME['LIVES'])
        shield = "|| Shield : " + ("Ready" if GAME['SHIELDREADY'] else "Not Ready")
        boss = ("|| Time Left : " + str(timeleft) if timeleft > 0 else "|| Boss Fight!!")
        bosslives = ("|| Boss Lives : " +str(GAME['BOSSLIVES']//BULLET['LENGTH']) if timeleft < 0 else " ")
        text = score + lives + shield + boss + bosslives
        self.matrix[2]=self.shownmatrix[2] = [i for i in (text + (GRID['WIDTH'] - len(text))*" ") ]
        for i in range(self.height):
            if i < GRID['ROOF']:
                print(colors.fg.lightcyan,'%s%s'% (pos(i,0),''.join(self.shownmatrix[i])))
            elif i > GRID['GROUND']:
                print(colors.fg.lightcyan,'%s%s'% (pos(i,0),''.join(self.shownmatrix[i])),colors.reset)
            else:
                continue
            # print('%s%s'% (pos(i,0),''.join(self.matrix[i])))

