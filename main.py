from getch import KBHit
from os import system
from mando import Player , Boss 
from objects import Bullet , Magnet , Snowball
from Obstacle import *
from ascii import yoda
from globals import mp , GRID , GAME , BULLETS , BULLET
system('tput civis')
system('clear')

kb = KBHit()
p1 = Player(6,6)

LASERS = [0 for _ in range(4)]
ltime, i = time(), 0

COINS = [0 for _ in range(4)]
ctime, j = time(), 0

SNOWBALLS = [ 0 for _ in range(4)]
btime , sn = time() , 0

cnt = 0

shuptime = 0
puptime = 0
powerupinterval = 0
magnettime = time()


while GAME['LIVES'] and GAME['BOSSLIVES']:
    # If not in boss phase
    if time() - gamestarttime < gametime:
        if time() - ltime > 1.4:
            ltime = time()
            if i < 4:
                LASERS[i] = Laser()
                i = i + 1
            else:
                if LASERS[i % 4].ycoord() < - 5:
                    LASERS[i % 4] = Laser()
                    i = i + 1
        else:
            if time() - ctime > 1.2:
                ctime = time()
                if j < 4:
                    COINS[j] = Coin()
                    j = j + 1
                else:
                    if COINS[j % 4].ycoord() < - 2:
                        COINS[j % 4] = Coin()
                        j = j + 1
        if time() - powerupinterval > 15:
            powerupinterval = time()
            pp = Speedup()

        if time() - magnettime > randint(20,30):
            magnettime = time()
            m = Magnet(GRID['ROOF'] - 3 , GRID['WIDTH'])
    elif time() - gamestarttime > gametime + 5:
        try :
            if boss:
                if time() - btime > 2:
                    btime = time()
                    if sn < 4:
                        SNOWBALLS[sn] = Snowball(boss.xcoord() + 5,boss.ycoord() - 2)
                        sn = sn + 1
                    else:
                        if SNOWBALLS[sn % 4].ycoord() < - 5:
                            SNOWBALLS[sn % 4] = Snowball(boss.xcoord() + 5,boss.ycoord() - 2)
                            sn = sn + 1
        except:
            btime = time()
            boss = Boss(min(p1.xcoord(),GRID['ROOF']),GRID['WIDTH'] - len(dragon[0]))

    mp.printmap()


    inp = kb.getinput()

    if inp is "q":
        system('clear')
        print("You didn't save Yoda :'(")
        system('tput cnorm')
        quit()
    
    if inp is " " and not p1.ondragon():
        if GAME['SHIELDREADY']:
            p1.shieldon()
            shuptime = time()
            GAME['SHIELDREADY'] = False
    

    if time() - shuptime > 60:
        GAME['SHIELDREADY'] = True

    if time() - shuptime > 10:
        p1.shieldoff()

    if p1.execute(inp):
        if k<4:
            BULLETS[k] = Bullet(p1.xcoord() + 1, p1.ycoord() + 8)
            k = k + 1
        else:
            if BULLETS[k%4].ycoord() > GRID['WIDTH']:
                BULLETS[k%4] = Bullet(p1.xcoord() + 1 , p1.ycoord() + 8)
                k = k + 1
    
    if time() - puptime > 10:
        GAME['SPEED'] = max(1,GAME['SPEED'] // 2)


# put every object after this
    try:
        m.update_matrix()
        if m.ycoord() < -5 :
            del m
        else :
            if p1.ycoord() > m.ycoord():
                p1.execute('aa')
            elif p1.ycoord() < m.ycoord():
                p1.execute('dd')
    except:
        pass

    for _ in BULLETS:
        try:
            _.update_matrix()
        except:
            pass
            
    for _ in LASERS:
        if not isinstance(_,int):
            laserupdate = _.update_matrix()
            if laserupdate is "Mando":
                p1.death()
            elif laserupdate is "Bullet":
                GAME['SCORE'] = GAME['SCORE'] + 1
    for _ in COINS:
        try:
                GAME['SCORE'] = GAME['SCORE'] + _.update_matrix()
        except:
            pass
    try :
        if boss.update(p1):
            sleep(5e-2)
            GAME['BOSSLIVES'] -= 1
    except:
        pass

    for _ in SNOWBALLS:
        try:
            if _.update_matrix():
                p1.death()
        except:
            pass

    try:
        if pp.update_matrix():
            GAME['SPEED'] = GAME['SPEED'] * 2
            puptime = time()
    except:
        pass
    sleep(1/30)

system('clear')
print("Game Over , Your Score Was : " , GAME['SCORE'])
if GAME['LIVES'] > 0:
    for i in yoda:
        print(i)
else:
    print("You didn't save Yoda :'(")
system('tput cnorm')
quit()