import os
from random import randint
from time import time , sleep
from colors import colors
from ascii import *
import numpy as np
def ll(off,num,factor):
    return np.linspace(0 + off , np.pi*factor + off , num )

def pos(x, y):
    return '\x1b[%d;%dH' % (x,y)

def pprint(self,color,i,j,x):
    print(color,'%s%s'% (pos(i,j),x),colors.reset)

def transpose(X):
    return [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]

def in_border(x, y):
    return GRID['GROUND'] <= x < GRID['ROOF'] and 0 <= y < GRID['WIDTH']

def check_collision(x, y):
    if mp.matrix[x][y] == "B":
        return "Bullet"
    if mp.matrix[x][y] in ['M','S']:
        return "Mando"
    return "Safe"

rows, columns = os.popen('stty size', 'r').read().split()
if int(columns) < 100 : 
    print("Increase Screen Size :)")
    quit()
    
gamestarttime = time()
gametime = 90
BULLETS = [0 for i in range(4)]
k = 0

# Map dimensions
GRID = {}
GRID['HEIGHT'] = int(rows)
GRID['WIDTH'] = int(columns)-2
GRID['GROUND'] = 6
GRID['ROOF'] = GRID['HEIGHT'] - 5

# Player
PLAYER = {}
PLAYER['RIGHTBORDER'] = (3*GRID['WIDTH'])//4
PLAYER['LEFTBORDER'] = 2
PLAYER['TOPBORDER'] = GRID['ROOF'] + 1 - len(mando)
PLAYER['BOTTOMBORDER'] = GRID['GROUND']

#Laser
LASER = {}
LASER['LENGTH'] = 5
LASER['ORIENTATION'] = [[1,0],[0,-1],[-1,1]]

#Coin
COIN = {}
COIN['LENGTH'] = 3

#Bullet
BULLET = {}
BULLET['LENGTH'] = 1
BULLET['WIDTH'] = 6

#Game
global GAME
GAME = {}
GAME['SCORE'] = 0
GAME['LIVES'] = 3
GAME['SPEED'] = 1 if int(columns) < 150 else 3
# while 1:
    # print(GAME['SPEED'])
GAME['SHIELD'] = False
GAME['SHIELDREADY'] = True
GAME['BOSSLIVES'] = 5 * BULLET['LENGTH']

#Magnet
MAGNET = {}
MAGNET['LENGTH'] = 3
MAGNET['WIDTH'] = 3

#Boss

#Dragon
DRAGON = {}
DRAGON['HEIGHT'] = 15
DRAGON['WIDTH'] = 15

#Snowball
SNOWBALL = {}
SNOWBALL['LENGTH'] = 2
SNOWBALL['WIDTH'] = 2
from map import map
mp = map()