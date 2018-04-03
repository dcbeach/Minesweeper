from tkinter import *
import random

width, height = 500, 500

gameboard = Tk()
gameboard.title("Minesweeper")
gameboard.geometry(str(width) + "x" + str(height) + "+200+200")

MINE_COUNT = 0
BOARD_SIZE = 20
TILE_COUNT = BOARD_SIZE * BOARD_SIZE
MULTIPLYER = int(width / BOARD_SIZE)

gameTiles = []
mineNumber = []
mineMap = []

def get_count(x,y):
    print("Getting Count of: " + "x = " + str(x) + " ," + "y = " + str(y))
    count = 0
    for [i,j] in mineMap:
        if (i - x <= 1 and i - x >= -1) and (j - y <= 1 and j - y >= -1):
            count += 1
    return count    

def set_zeros(x,y):
    print("x = " + str(x) + " ," + "y = " + str(y))
    check_left(x,y)
    check_right(x,y)
    check_up(x,y)
    check_down(x,y)

    
def check_left(x,y):
    if get_count(x-1,y) == 0 and x-1 >= 0:
        print("Checking left")
        gameTiles[x-1][y].config(text='0')
        check_left(x-1,y)
    else:
        check_up(x-1,y)
        check_down(x-1,y)

def check_right(x,y):
    if get_count(x+1,y) == 0 and x+1 <= BOARD_SIZE-1:
        print("Checking right")
        gameTiles[x+1][y].config(text='0')
        check_right(x+1,y)
    else:
        check_up(x+1,y)
        check_down(x+1,y)

def check_up(x,y):
    if get_count(x,y-1) == 0 and y-1 >= 0:
        print("Checking up")
        gameTiles[x][y-1].config(text='0')
        check_up(x,y-1)
    else:
        check_left(x,y-1)
        check_right(x,y-1)

def check_down(x,y):
    if get_count(x,y+1) == 0 and y+1 <= BOARD_SIZE-1:
        print("Checking down")
        gameTiles[x][y+1].config(text='0')
        check_down(x,y+1)
    else:
        check_left(x,y+1)
        check_right(x,y+1)
'''
def check_upleft(x,y):
    if get_count(x-1,y-1) == 0 and y-1 >= 0 and x-1 >=0:
        print("Checking upleft")
        gameTiles[x-1][y-1].config(text='0')
        check_upleft(x-1,y-1)

def check_upright(x,y):
    if get_count(x+1,y-1) == 0 and y-1 >= 0 and x+1 <= BOARD_SIZE-1:
        print("Checking up")
        gameTiles[x+1][y-1].config(text='0')
        check_upright(x+1,y-1)

def check_downleft(x,y):
    if get_count(x-1,y+1) == 0 and y+1 <= BOARD_SIZE-1 and x-1 >= 0:
        print("Checking down")
        gameTiles[x-1][y+1].config(text='0')
        check_downleft(x-1,y+1)

def check_downright(x,y):
    if get_count(x+1,y+1) == 0 and y+1 <= BOARD_SIZE-1 and x+1 <= BOARD_SIZE-1:
        print("Checking down")
        gameTiles[x+1][y+1].config(text='0')
        check_downright(x+1,y+1)
'''

def unearth_tile(x, y):
    if [x,y] in mineMap:
        gameTiles[x][y].config(text='M')
    else:
        count = get_count(x,y)
        if count != 0:       
            gameTiles[x][y].config(text=str(count))        
        else:
            gameTiles[x][y].config(text=str(count))
            set_zeros(x,y)

for mine in range(MINE_COUNT):
    while True:
        tile = random.randint(0,TILE_COUNT-1)
        if tile not in mineNumber:
            mineNumber.append(tile)
            break

for mine in mineNumber:
    x = mine % BOARD_SIZE
    y = int(mine/BOARD_SIZE)
    mineMap.append([x,y])
    
                
for x in range(BOARD_SIZE):
    gameTiles.append([])
    for y in range(BOARD_SIZE):
        gameTiles[x].append(Button(gameboard, command=(lambda i=x,j=y: unearth_tile(i,j))))
        gameTiles[x][y].place(x=MULTIPLYER*x, y=MULTIPLYER*y, width=MULTIPLYER, height=MULTIPLYER)

        
gameboard.mainloop()
