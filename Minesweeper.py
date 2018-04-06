from tkinter import *
import random

width, height = 500, 500

gameboard = Tk()
gameboard.title("Minesweeper")
gameboard.geometry(str(width) + "x" + str(height) + "+200+200")

MINE_COUNT = 40
BOARD_SIZE = 20
TILE_COUNT = BOARD_SIZE * BOARD_SIZE
MULTIPLYER = int(width / BOARD_SIZE)

gameTiles = []
mineNumber = []
mineMap = []
clicked = []


def get_count(x, y):
    count = 0
    for [i, j] in mineMap:
        if (-1 <= i - x <= 1) and (-1 <= j - y <= 1):
            count += 1
    return count    


def set_zeros(x,y):
    _x = x
    _y = y

    tochecklist = []
    tochecklist.append([x,y])

    while len(tochecklist) != 0:
        current = tochecklist.pop()
        print("After pop: " + str(len(tochecklist)))
        check_up(current, tochecklist)
        check_down(current, tochecklist)
        check_left(current, tochecklist)
        check_right(current, tochecklist)
        check_upleft(current, tochecklist)
        check_downright(current, tochecklist)
        check_downleft(current, tochecklist)
        check_upright(current, tochecklist)
        print(len(tochecklist))


def check_left(current, list):
    x = current[0]
    y = current[1]
    if [x-1, y] not in clicked:
        if get_count(x-1, y) == 0 and x-1 > 0:
            gameTiles[x-1][y].config(text='0')
            clicked.append([x-1, y])
            list.append([x-1, y])
        elif x-1 < 0:
            return None
        else:
            gameTiles[x-1][y].config(text=str(get_count(x-1, y)))



def check_right(current,list):
    x = current[0]
    y = current[1]
    if [x + 1, y] not in clicked:
        if get_count(x+1, y) == 0 and x+1 <= BOARD_SIZE-1:
            gameTiles[x+1][y].config(text='0')
            clicked.append([x + 1, y])
            list.append([x + 1, y])
        elif x+1 > BOARD_SIZE-1:
            return None
        else:
            gameTiles[x+1][y].config(text=str(get_count(x+1, y)))



def check_up(current,list):
    x = current[0]
    y = current[1]
    if [x, y - 1] not in clicked:
        if get_count(x, y-1) == 0 and y-1 >= 0:
            gameTiles[x][y-1].config(text='0')
            clicked.append([x, y - 1])
            list.append([x, y-1])
        elif y-1 < 0:
            return None
        else:
            gameTiles[x][y-1].config(text=str(get_count(x, y-1)))



def check_down(current,list):
    x = current[0]
    y = current[1]
    if [x, y + 1] not in clicked:
        if get_count(x, y+1) == 0 and y+1 <= BOARD_SIZE-1:
            gameTiles[x][y+1].config(text='0')
            clicked.append([x, y + 1])
            list.append([x, y+1])
        elif y+1 > BOARD_SIZE-1:
            return None
        else:
            gameTiles[x][y+1].config(text=str(get_count(x, y+1)))


def check_upleft(current, list):
    x = current[0]
    y = current[1]
    if [x - 1, y - 1] not in clicked:
        if get_count(x-1, y-1) == 0 and y-1 >= 0 and x-1 >= 0:
            gameTiles[x-1][y-1].config(text='0')
            clicked.append([x - 1, y - 1])
            list.append([x - 1, y-1])
        elif x-1 < 0 or y-1 < 0:
            return None
        else:
            gameTiles[x - 1][y - 1].config(text=str(get_count(x-1, y-1)))


def check_upright(current,list):
    x = current[0]
    y = current[1]
    if [x + 1, y - 1] not in clicked:
        if get_count(x+1, y-1) == 0 and y-1 >= 0 and x+1 <= BOARD_SIZE-1:
            gameTiles[x+1][y-1].config(text='0')
            clicked.append([x + 1, y + 1])
            list.append([x + 1, y-1])
        elif y-1 < 0 or x+1 > BOARD_SIZE-1:
            return None
        else:
            gameTiles[x + 1][y - 1].config(text=str(get_count(x+1, y+1)))


def check_downleft(current,list):
    x = current[0]
    y = current[1]
    if [x - 1, y + 1] not in clicked:
        if get_count(x-1,y+1) == 0 and y+1 <= BOARD_SIZE-1 and x-1 >= 0:
            gameTiles[x-1][y+1].config(text='0')
            clicked.append([x - 1, y + 1])
            list.append([x - 1, y+1])
        elif y+1 > BOARD_SIZE-1 or x-1 < 0:
            return None
        else:
            gameTiles[x - 1][y +1].config(text=str(get_count(x-1,y+1)))


def check_downright(current, list):
    x = current[0]
    y = current[1]
    if [x + 1, y + 1] not in clicked:
        if get_count(x+1,y+1) == 0 and y+1 <= BOARD_SIZE-1 and x+1 <= BOARD_SIZE-1:
            gameTiles[x+1][y+1].config(text='0')
            clicked.append([x + 1, y + 1])
            list.append([x +1, y+1])
        elif y+1 > BOARD_SIZE-1 or x+1 > BOARD_SIZE-1:
            return None
        else:
            gameTiles[x + 1][y + 1].config(text=str(get_count(x+1,y+1)))


def reveal_tile(x,y):
    if [x,y] in mineMap:
        gameTiles[x][y].config(text='M')
    else:
        count = get_count(x, y)
        if count != 0:       
            gameTiles[x][y].config(text=str(count))        
        else:
            gameTiles[x][y].config(text=str(count))
            set_zeros(x, y)


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
        gameTiles[x].append(Button(gameboard, command=(lambda i=x,j=y: reveal_tile(i,j))))
        gameTiles[x][y].place(x=MULTIPLYER*x, y=MULTIPLYER*y, width=MULTIPLYER, height=MULTIPLYER)

        
gameboard.mainloop()
