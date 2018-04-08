from tkinter import *
import random
import tkinter as tk
from tkinter import font as tkfont
import sqlite3


def initialize_variables():
    global width, height, MINE_COUNT, BOARD_SIZE, TILE_COUNT, MULTIPLYER, CLICKS
    global timer, gameover, win, gameTiles, mineNumber, mineMap, clicked
    width, height = 500, 550
    win = 0
    BOARD_SIZE = 10

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(str(width) + "x" + str(height) + "+200+200")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, GameBoard, HighScore):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage", 0, 0)

    def show_frame(self, page_name, mine_count, board_size):
        for frame in self.frames.values():
            frame.grid_remove()
            for widget in frame.winfo_children():
                widget.destroy()

        if page_name == 'GameBoard':
            self.frames[page_name].start_game(mine_count, board_size)
        elif page_name == 'HighScore':
            self.frames[page_name].display_highscores()
        elif page_name == 'StartPage':
            self.frames[page_name].display_startpage()

        frame = self.frames[page_name]
        frame.grid()
        frame.winfo_toplevel().geometry("500x550+200+200")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def display_startpage(self):
        label = tk.Label(self, text="Welcome to Minesweeper!", font=self.controller.title_font)
        label.place(relx=.10, rely=.1, width=.8 * width)

        easymode = tk.Button(self, text="Play Easy", width=10, height=2, font=("Helvetica", 20),
                            command=lambda: [self.controller.show_frame("GameBoard", 15, 10)], bg='skyblue1')
        mediummode = tk.Button(self, text="Play Medium", width=10, height=2, font=("Helvetica", 20),
                             command=lambda: [self.controller.show_frame("GameBoard", 50, 15)], bg='dark orange')
        hardmode = tk.Button(self, text="Play Hard",  width=10, height=2, font=("Helvetica", 20),
                             command=lambda: [self.controller.show_frame("GameBoard", 100, 20)], bg='red3')
        highscore = tk.Button(self, text="High Scores", width=10, height=2, font=("Helvetica", 20),
                            command=lambda: self.controller.show_frame("HighScore", 0, 0))

        easymode.place(relx=.25, rely=.2, width=.5 * width)
        mediummode.place(relx=.25, rely=.4, width=.5 * width)
        hardmode.place(relx=.25, rely=.6, width=.5 * width)
        highscore.place(relx=.25, rely=.8, width=.5 * width)


class GameBoard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def start_game(self, mine_count, board_size):
        global width, height, MINE_COUNT, BOARD_SIZE, TILE_COUNT, MULTIPLYER, CLICKS, TOP_SCORES, flagmode_button, name_entry
        global timer, gameover, win, gameTiles, mineNumber, mineMap, clicked, timer_label, FLAG_MODE, player_name

        timer = 0
        gameover = False
        win = -1

        FLAG_MODE = False
        TOP_SCORES = []
        gameTiles = []
        mineNumber = []
        mineMap = []
        clicked = []

        BOARD_SIZE= board_size
        MINE_COUNT = mine_count
        TILE_COUNT = board_size * board_size
        MULTIPLYER = int(width / board_size)
        TILE_RELX_POS = 100 / board_size * .01
        TILE_RELY_POS = (100 * .91) / board_size * .01

        timer_label = Label(self, text='Score: ', font=('Helvetica', 20))
        timer_label.place(relx=.05, rely=.01)
        name_entry = Entry(self, text="Name Here")
        name_entry.place(relx=.4, rely=.01, width=100)
        flagmode_button = Button(self, text='Flag Mode Off', command=lambda: self.change_flagmode())
        flagmode_button.place(relx=.8, rely=.02, width=.20 * width)

        for mine in range(mine_count):
            while True:
                tile = random.randint(0, TILE_COUNT - 1)
                if tile not in mineNumber:
                    mineNumber.append(tile)
                    break

        for mine in mineNumber:
            x = mine % board_size
            y = int(mine / board_size)
            mineMap.append([x, y])

        for x in range(board_size):
            gameTiles.append([])
            for y in range(board_size):
                gameTiles[x].append(Button(self, command=(lambda i=x, j=y: [self.reveal_tile(i, j), self.check_clicked(i, j)])))
                gameTiles[x][y].place(relx=TILE_RELX_POS*x, rely=0.09 + TILE_RELY_POS*y,
                                      width=MULTIPLYER, height=MULTIPLYER)

    def change_flagmode(self):
        global FLAG_MODE, flagmode_button
        if FLAG_MODE:
            FLAG_MODE = False
            flagmode_button.config(text="Flag Mode Off")
        else:
            FLAG_MODE = True
            flagmode_button.config(text="Flag Mode On")

    def check_clicked(self, x, y):
        if len(clicked) == BOARD_SIZE * BOARD_SIZE - MINE_COUNT:
            global gameover
            global win
            win = 1


    def update_clock(self):
        global timer_label, name_entry, player_name
        global timer, win
        global gameover

        if not gameover:
            count = 0
            for columns in gameTiles:
                for tile in columns:
                    if tile.cget('text') != '':
                        count += 1
            print(count)
            if count == BOARD_SIZE * BOARD_SIZE - MINE_COUNT:
                gameover = True
            timer += 1
            timer_label.configure(text="Score: " + str(timer))
            self.after(1000, self.update_clock)
        else:
            print('You WON')
            win = 1
            player_name = name_entry.get()
            self.after(1000, self.controller.show_frame("HighScore", 0, 0))


    def get_count(self, x, y):
        count = 0
        for [i, j] in mineMap:
            if (-1 <= i - x <= 1) and (-1 <= j - y <= 1):
                count += 1
        return count

    def set_zeros(self, x, y):
        _x = x
        _y = y

        tochecklist = []
        tochecklist.append([x, y])

        while len(tochecklist) != 0:
            current = tochecklist.pop()
            self.check_up(current, tochecklist)
            self.check_down(current, tochecklist)
            self.check_left(current, tochecklist)
            self.check_right(current, tochecklist)
            self.check_upleft(current, tochecklist)
            self.check_downright(current, tochecklist)
            self.check_downleft(current, tochecklist)
            self.check_upright(current, tochecklist)

    def check_left(self, current, list):
        x = current[0]
        y = current[1]
        if [x - 1, y] not in clicked:
            if self.get_count(x - 1, y) == 0 and x - 1 > 0:
                gameTiles[x - 1][y].config(text='0', bg="grey")
                clicked.append([x - 1, y])
                list.append([x - 1, y])
            elif x - 1 < 0:
                return None
            else:
                clicked.append([x - 1, y])
                gameTiles[x - 1][y].config(text=str(self.get_count(x - 1, y)))

    def check_right(self, current, list):
        x = current[0]
        y = current[1]
        if [x + 1, y] not in clicked:
            if self.get_count(x + 1, y) == 0 and x + 1 <= BOARD_SIZE - 1:
                gameTiles[x + 1][y].config(text='0', bg="grey")
                clicked.append([x + 1, y])
                list.append([x + 1, y])
            elif x + 1 > BOARD_SIZE - 1:
                return None
            else:
                clicked.append([x + 1, y])
                gameTiles[x + 1][y].config(text=str(self.get_count(x + 1, y)))

    def check_up(self, current, list):
        x = current[0]
        y = current[1]
        if [x, y - 1] not in clicked:
            if self.get_count(x, y - 1) == 0 and y - 1 >= 0:
                gameTiles[x][y - 1].config(text='0', bg="grey")
                clicked.append([x, y - 1])
                list.append([x, y - 1])
            elif y - 1 < 0:
                return None
            else:
                clicked.append([x, y - 1])
                gameTiles[x][y - 1].config(text=str(self.get_count(x, y - 1)))

    def check_down(self, current, list):
        x = current[0]
        y = current[1]
        if [x, y + 1] not in clicked:
            if self.get_count(x, y + 1) == 0 and y + 1 <= BOARD_SIZE - 1:
                gameTiles[x][y + 1].config(text='0', bg="grey")
                clicked.append([x, y + 1])
                list.append([x, y + 1])
            elif y + 1 > BOARD_SIZE - 1:
                return None
            else:
                clicked.append([x, y + 1])
                gameTiles[x][y + 1].config(text=str(self.get_count(x, y + 1)))

    def check_upleft(self, current, list):
        x = current[0]
        y = current[1]
        if [x - 1, y - 1] not in clicked:
            if self.get_count(x - 1, y - 1) == 0 and y - 1 >= 0 and x - 1 >= 0:
                gameTiles[x - 1][y - 1].config(text='0', bg="grey")
                clicked.append([x - 1, y - 1])
                list.append([x - 1, y - 1])
            elif x - 1 < 0 or y - 1 < 0:
                return None
            else:
                clicked.append([x - 1, y - 1])
                gameTiles[x - 1][y - 1].config(text=str(self.get_count(x - 1, y - 1)))

    def check_upright(self, current, list):
        x = current[0]
        y = current[1]
        if [x + 1, y - 1] not in clicked:
            if self.get_count(x + 1, y - 1) == 0 and y - 1 >= 0 and x + 1 <= BOARD_SIZE - 1:
                gameTiles[x + 1][y - 1].config(text='0', bg="grey")
                clicked.append([x + 1, y + 1])
                list.append([x + 1, y - 1])
            elif y - 1 < 0 or x + 1 > BOARD_SIZE - 1:
                return None
            else:
                clicked.append([x + 1, y + 1])
                gameTiles[x + 1][y - 1].config(text=str(self.get_count(x + 1, y - 1)))

    def check_downleft(self, current, list):
        x = current[0]
        y = current[1]
        if [x - 1, y + 1] not in clicked:
            if self.get_count(x - 1, y + 1) == 0 and y + 1 <= BOARD_SIZE - 1 and x - 1 >= 0:
                gameTiles[x - 1][y + 1].config(text='0', bg="grey")
                clicked.append([x - 1, y + 1])
                list.append([x - 1, y + 1])
            elif y + 1 > BOARD_SIZE - 1 or x - 1 < 0:
                return None
            else:
                clicked.append([x - 1, y + 1])
                gameTiles[x - 1][y + 1].config(text=str(self.get_count(x - 1, y + 1)))

    def check_downright(self, current, list):
        x = current[0]
        y = current[1]
        if [x + 1, y + 1] not in clicked:
            if self.get_count(x + 1, y + 1) == 0 and y + 1 <= BOARD_SIZE - 1 and x + 1 <= BOARD_SIZE - 1:
                gameTiles[x + 1][y + 1].config(text='0', bg="grey")
                clicked.append([x + 1, y + 1])
                list.append([x + 1, y + 1])
            elif y + 1 > BOARD_SIZE - 1 or x + 1 > BOARD_SIZE - 1:
                return None
            else:
                clicked.append([x + 1, y + 1])
                gameTiles[x + 1][y + 1].config(text=str(self.get_count(x + 1, y + 1)))

    def reveal_tile(self, x, y):
        if len(clicked) == 0:
            self.update_clock()
        if [x, y] in mineMap:
            global gameover
            global win
            if FLAG_MODE:
                if gameTiles[x][y].cget('bg') != 'SystemButtonFace':
                    gameTiles[x][y].config(text='', bg='SystemButtonFace')
                else:
                    gameTiles[x][y].config(text='', bg='blue')
            else:
                gameover = True
                win = 0
                gameTiles[x][y].config(text='M')
                self.controller.show_frame("HighScore", 0, 0)
        else:
            count = self.get_count(x, y)
            if [x, y] not in clicked:
                clicked.append([x, y])
            if FLAG_MODE:
                if gameTiles[x][y].cget('bg') != 'SystemButtonFace':
                    gameTiles[x][y].config(text='', bg='SystemButtonFace')
                else:
                    gameTiles[x][y].config(text='', bg='blue')
            else:
                if gameTiles[x][y].cget('bg') != 'SystemButtonFace':
                    gameTiles[x][y].config(text='', bg='SystemButtonFace')
                if count != 0:
                    gameTiles[x][y].config(text=str(count))
                else:
                    gameTiles[x][y].config(text=str(count), bg='grey')
                    self.set_zeros(x, y)


class HighScore(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def display_highscores(self):
        self.create_highscore_table()

        winlose_title = tk.Label(self, text="You won/lost", font=('Helvetica', 25))
        winlose_title.place(relx=.1, rely=.1, width=.8 * width)
        global win, TOP_SCORES, player_name
        if win == 1:
            winlose_title.config(text="You Won! : " + str(timer) + " Seconds")
            self.score_entry()
        elif win == 0:
            winlose_title.config(text="You Lost!")
        elif win == -1:
            winlose_title.config(text="")
        win = -1

        highscore_title = tk.Label(self, text="High Scores", font=self.controller.title_font)
        highscore_title.place(relx=.25, rely=.25, width=.5 * width)

        TOP_SCORES = self.get_top_scores()
        for passnum in range(len(TOP_SCORES) - 1, 0, -1):
            for i in range(passnum):
                if TOP_SCORES[i] > TOP_SCORES[i + 1]:
                    temp = TOP_SCORES[i]
                    TOP_SCORES[i] = TOP_SCORES[i + 1]
                    TOP_SCORES[i + 1] = temp

        score_labels = []
        for i in range(5):
            print(i)
            score_labels.append(tk.Label(self, text="Name: Score", font=self.controller.title_font))
            score_labels[i].place(relx=.25, rely=.35 + (i * .1), width=.5 * width)
            if len(TOP_SCORES) > i:
                score_labels[i].config(text=str(TOP_SCORES[i][0]) + ": " + str(TOP_SCORES[i][1]) + " Seconds")

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: self.controller.show_frame("StartPage", 0, 0))
        button.place(relx=.25, rely=.9, width=.5 * width)

    def get_top_scores(self):
        score_list = []
        conn = sqlite3.connect('msScores.db')
        c = conn.cursor()
        c.execute("SELECT * FROM scores WHERE difficulty=?", (str(BOARD_SIZE),))
        rows = c.fetchall()
        for row in rows:
            score_list.append([row[0], row[1]])
        return score_list

    def create_highscore_table(self):
        conn = sqlite3.connect('msScores.db')
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS scores(playerName TEXT, score INTEGER, difficulty INTEGER)')

    def score_entry(self):
        conn = sqlite3.connect('msScores.db')
        c = conn.cursor()
        c.execute("INSERT INTO scores(playerName, score, difficulty) VALUES(?,?,?)",
                  (player_name, timer, BOARD_SIZE))
        conn.commit()

if __name__ == "__main__":
    initialize_variables()
    app = SampleApp()
    app.mainloop()











