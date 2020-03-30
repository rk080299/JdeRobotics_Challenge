from functools import reduce
from itertools import product
from operator import add
from random import sample
from tkinter import Button, Frame, Label, StringVar, Tk
from typing import Set, Tuple
from tkinter import *

#global
Width = 3
Height = 1

class Model:
    def __init__(self, width: int):
        self.width = width
        self.grid = self.create_grid()

    def create_grid(self):
        return [[0] * self.width for _ in range(self.width)]

class View(Frame):
    def __init__(self, master:Tk, width: int):
        Frame.__init__(self, master)
        self.master = master
        self.width = width
        self.master.title('Game Of Life')
        self.grid()
        self.top_panel = TopPanel(self.master,self.width)
        self.buttons = self.cell_buttons()

    def cell_buttons(self):
        def cell_button(x, y):
            button = Button(self.master, width=Width,height=Height, bg='white')
            button.grid(row=x + 1, column=y + 1)
            return button

        return [[cell_button(x, y) for y in range(self.width)] for x in range(self.width)]


def get_adjacent(index: Tuple[int, int]) -> Set[Tuple[int, int]]:
    x, y = index

    return {
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
    }

class TopPanel(Frame):
    def __init__(self,master:Tk, width: int):
        Frame.__init__(self, master)
        self.master = master
        self.grid()

        self.reset_button = Button(self.master, width = 5,text='Reset')
        self.reset_button.grid(row=0, column = 12, columnspan=4)

        #start button here
        self.start_button = Button(self.master, text = "Start Game")#, command = self.simulate_game)
        self.start_button.grid(row = 0, column = 5, columnspan = 4)


class Controls(object):
    def __init__(self, width: int):
        self.width = width
        self.height = width
        self.model = Model(self.width)
        self.root = Tk()
        self.view = View(self.root, self.width)
        self.color_dict = {
            0: 'white', 1: 'black'
        }
        self.count = set()
        self.cells_live = set()
        self.game_state = None

        self.size_x = width - 2
        self.size_y = width - 2
        self.generate_next = True
        self.initialize_bindings()
        self.root.mainloop()


    def initialize_bindings(self):
        for x in range(self.height):
            for y in range(self.width):
                def closure_helper(f, index):
                    def g(_): f(index)

                    return g


                self.view.buttons[x][y].bind('<Button-1>', closure_helper(self.reveal, (x, y)))

                self.view.buttons[x][y].bind('<Button-3>', closure_helper(self.reveal, (x, y)))

        # Set up reset button
        self.view.top_panel.reset_button.bind('<Button>', lambda event: self.reset())

        self.view.top_panel.start_button.bind('<Button>', lambda event: self.simulate_game())

    def reset(self):
    	self.generate_next = False
     

    def reveal(self, index: Tuple[int, int]):
        x, y = index

        bt_color = self.view.buttons[x][y].cget('bg')
        if bt_color == 'white':
            self.view.buttons[x][y].configure(fg=self.color_dict[0], bg='black')
        else:
            self.view.buttons[x][y].configure(fg=self.color_dict[1], bg='white')


#-----GAME LOGIC-----------------------------------------------------------------------------------------
    def cell_toggle(self, cell):
        if cell['bg'] == "white":
            cell['bg'] = "black"
        else:
            cell['bg'] = "white"

    def simulate_game(self):
        self.disable_buttons()

        buttons_to_toggle = []
        for i in range(1, self.size_y + 1):
            for j in range(1, self.size_x + 1):
                coord = (i, j)

                if(self.view.buttons[i][j]['bg'] == "white" and self.neighbor_count(i, j) == 3):
                    buttons_to_toggle.append(coord)

                elif self.view.buttons[i][j]['bg'] == "black" and self.neighbor_count(i, j) != 3 and self.neighbor_count(i, j) != 2:
                    buttons_to_toggle.append(coord)


        for coord in buttons_to_toggle:
            self.cell_toggle(self.view.buttons[coord[0]][coord[1]])

        if self.generate_next:
            self.view.after(100, self.simulate_game)
        else:
            self.enable_buttons()

    def disable_buttons(self):
        if self.view.buttons[1][1]['state'] != DISABLED:
            for i in range(0, self.size_y + 2):
                for j in range(0, self.size_x + 2):
                    self.view.buttons[i][j].configure(state = DISABLED)

            self.view.top_panel.reset_button.configure(state = NORMAL)
            self.view.top_panel.start_button.configure(state = DISABLED)

    def enable_buttons(self):
        # resets game
        for i in range(0, self.size_y + 2):
            for j in range(0, self.size_x + 2):
                self.view.buttons[i][j]['bg'] = "white"
                self.view.buttons[i][j].configure(state = NORMAL)

        self.view.top_panel.reset_button.configure(state = DISABLED)
        self.view.top_panel.start_button.configure(state = NORMAL)
        self.generate_next = True

    def neighbor_count(self, x_coord, y_coord):
        count = 0
        for i in range(x_coord - 1, x_coord + 2):
            for j in range(y_coord - 1, y_coord + 2):
                if (i != x_coord or j != y_coord) and self.view.buttons[i][j]['bg'] == "black":
                    count += 1

        return count




if __name__ == '__main__':
    n = input('Enter number of rows(15 or 30 or 45): ')

    Controls(*{
        '15': (15,),
        '30': (30,),
        '45': (45,)
    }[n.lower()])
