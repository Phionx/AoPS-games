# Python Class 2344
# Lesson 10 Problem 1
# Author: snowapple (471208)

import random
from tkinter import *
import tkinter.messagebox as messagebox


class MinesweeperCell(Label):
    def __init__(self, master, coord):
        Label.__init__(
            self, master, height=1, width=2, text="", bg="white", font=("Arial", 24)
        )
        self.colormap = [
            "",
            "blue",
            "darkgreen",
            "red",
            "purple",
            "maroon",
            "cyan",
            "black",
            "dim gray",
        ]
        self.master = master
        self.coord = coord
        self.isBomb = False
        self.isExposed = False
        self.isFlagged = False
        self.numBombs = None
        self["relief"] = RAISED
        self.bind("<Button-1>", self.left_click)
        self.bind("<Button-2>", self.right_click)

    def left_click(self, event):
        # simply expose
        # if bomb, end game
        if not self.master.gameover and not self.isFlagged:
            if not self.isBomb:
                self.expose()
            else:
                self.master.gameover = True
                self.master.bomb_detonation()

    def expose(self):
        if not self.isExposed and not self.isFlagged:
            self.isExposed = True
            self["text"] = str(self.numBombs) if self.numBombs != 0 else ""
            self["bg"] = "lightgrey"
            self["relief"] = SUNKEN
            self.master.unexposed_safe_cells -= 1
            if self.master.unexposed_safe_cells == 0:
                self.master.gameover = True
                self.master.game_won()
            if self.numBombs == 0:
                self.master.expose_neighbors(self.coord)
            else:
                self["fg"] = self.colormap[self.numBombs]

    def right_click(self, event):
        # if exposed, cannot flag
        # if not exposed, flag
        if not self.isExposed and not self.master.gameover:
            self.isFlagged = not self.isFlagged
            self["text"] = "*" if self.isFlagged else ""
            self.master.flaggedCells += 1 if self.isFlagged else -1
            self.master.update_score()

    def expose_bomb(self):
        if not self.isFlagged:
            self["bg"] = "red"
            self["text"] = "*"
        else:  # shows user which bombs they flagged correctly, because the user can flag incorrectly
            self["bg"] = "yellow"
            self["text"] = "*"


class Minesweeper(Frame):
    def __init__(self, master, width, height, numBombs):
        self.height = height
        self.width = width
        self.unexposed_safe_cells = width * height - numBombs
        self.numBombs = numBombs
        self.flaggedCells = 0
        self.gameover = False
        # Setup GUI
        # initialize a new Frame
        Frame.__init__(self, master, bg="black")
        self.grid()
        # put in lines between the cells (not necessary)
        # (odd numbered rows and columns in the grid)
        # for c in range(1, 2 * (self.width - 1), 2):
        #     self.columnconfigure(c, minsize=3)
        # for r in range(1, 2 * (self.height - 1), 2):
        #     self.rowconfigure(r, minsize=3)

        # Setup score Label
        self.scoreLabel = Label(
            self, height=1, width=2, text="", bg="white", font=("Arial", 24)
        )

        self.scoreLabel.grid(row=2 * self.height, column=self.width - 2)
        self.scoreLabel["text"] = str(self.numBombs - self.flaggedCells)

        # Setup Board
        self.board = {}  # key: (row_index, col_index), val: MinesweeperCell object
        for row in range(self.height):
            for col in range(self.width):
                loc = (row, col)
                self.board[loc] = MinesweeperCell(self, loc)
                self.board[loc].grid(row=2 * row, column=2 * col)

        # Setup Bombs
        self.bombCells = random.sample(list(self.board.values()), numBombs)
        for cell in self.bombCells:
            cell.isBomb = True

        for row in range(self.height):
            for col in range(self.width):
                self.find_num_bombs((row, col))

    def find_num_bombs(self, coord):
        row, col = coord
        validNeighbors = self.find_neighbors(coord)
        numBombs = 0
        for loc in validNeighbors:  # loc = (r,c)
            cell = self.board[loc]
            numBombs += 1 if cell.isBomb else 0
        self.board[(row, col)].numBombs = numBombs

    def find_neighbors(self, coord):
        row, column = coord
        neighIndicies = [
            (row - 1, column - 1),
            (row - 1, column),
            (row - 1, column + 1),
            (row, column + 1),
            (row, column - 1),
            (row + 1, column),
            (row + 1, column + 1),
            (row + 1, column - 1),
        ]

        validNeighbors = []
        for (r, c) in neighIndicies:
            if 0 <= r and r < self.height:
                if 0 <= c and c < self.width:
                    validNeighbors.append((r, c))

        return validNeighbors

    def expose_neighbors(self, coord):
        validNeighbors = self.find_neighbors(coord)
        for loc in validNeighbors:
            cell = self.board[loc]
            cell.expose()

    def bomb_detonation(self):
        messagebox.showerror("Minesweeper", "KABOOM! You lose.", parent=self)
        for cell in self.bombCells:
            cell.expose_bomb()

    def game_won(self):
        messagebox.showinfo("Minesweeper", "Congratulations -- you won!", parent=self)

    def update_score(self):
        self.scoreLabel["text"] = str(self.numBombs - self.flaggedCells)


def play_minesweeper(width, height, numBombs):
    root = Tk()
    root.title("Minesweeper")
    mn = Minesweeper(root, width, height, numBombs)
    root.mainloop()


play_minesweeper(12, 10, 15)

