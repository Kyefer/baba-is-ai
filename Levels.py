
import os
from tkinter import Tk, Label, Entry, Button, Menu, Listbox, Frame
import tkinter.filedialog as fd
import numpy as np

from Game import Entity, Level, Object, Modifier, Link


levels = []


def level00():
    level = Level("00", 33, 18)
    level.setup_entities({
        (11, 6): Entity.NOUN(Object.BABA),
        (12, 6): Entity.IS(),
        (13, 6): Entity.MOD(Modifier.YOU),
        (19, 6): Entity.NOUN(Object.FLAG),
        (20, 6): Entity.IS(),
        (21, 6): Entity.MOD(Modifier.WIN),

        # (7, 20): Entity.OBJ(Object.BABA),

        (11, 14): Entity.NOUN(Object.WALL),
        (12, 14): Entity.IS(),
        (13, 14): Entity.MOD(Modifier.STOP),
        (19, 14): Entity.NOUN(Object.ROCK),
        (20, 14): Entity.IS(),
        (21, 14): Entity.MOD(Modifier.PUSH),
    })

    walls = {}
    for i in range(11):
        walls[(i + 11, 8)] = Object.WALL
        walls[(i + 11, 12)] = Object.WALL
    level.setup_objects(walls)

    level.setup_objects({
        (16, 9): Object.ROCK,
        (16, 10): Object.ROCK,
        (16, 11): Object.ROCK,
        (12, 10): Object.BABA,
        (20, 10): Object.FLAG,
    })

    return level


def level01():
    level = Level("01", 24, 18)
    level.setup_entities({
        (8, 7): Entity.NOUN(Object.FLAG),

    })


levels.append(level00())


def get_values():
    vals = ["", Link.IS.name, Link.AND.name]
    vals += [obj.name for obj in list(Object)]
    vals += [obj.name.lower() for obj in list(Object)]
    vals += [mod.name for mod in list(Modifier)]
    return vals


class Editor:
    def __init__(self, parent):
        self.board: np.ndarray = None

        self.parent = parent

        self.menu = None
        self.filemenu = None
        self.filename: str = None

        self.dim_frame = None
        self.x_ent = None
        self.y_ent = None
        self.set_btn = None

        self.tile_frame = None
        self.grid = None

        self.create_gui()

    def create_gui(self):
        self.parent.title("Baba is You Level Editor")

        self.menu = Menu(self.parent)
        self.parent.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label='Open...', command=self.open_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Save', state="disabled", command=self.save_file)
        self.filemenu.add_command(label='Save As...', state="disabled", command=self.save_as_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.parent.quit)

        self.dim_frame = Frame(self.parent)
        self.dim_frame.grid(row=0, column=0)

        Label(self.dim_frame, text="x").grid(row=0, column=0)
        Label(self.dim_frame, text="y").grid(row=0, column=2)
        self.x_ent = Entry(self.dim_frame)
        self.y_ent = Entry(self.dim_frame)

        self.x_ent.insert(0, 4)
        self.y_ent.insert(0, 3)

        self.x_ent.grid(row=0, column=1)
        self.y_ent.grid(row=0, column=3)

        self.set_btn = Button(self.dim_frame, text="SET", width=10, command=self.set_dim)
        self.set_btn.grid(row=0, column=5)

    def set_dim(self):
        try:
            w, h = int(self.x_ent.get()), int(self.y_ent.get())
            self.board = np.empty(shape=(w, h), dtype=object)
            for i in range(w):
                for j in range(h):
                    self.board[i][j] = ""
            self.load_board()
            self.filemenu.entryconfig("Save As...", state="normal")
        except ValueError:
            return

    def load_board(self):
        if self.tile_frame:
            self.tile_frame.grid_forget()
        self.tile_frame = Frame(self.parent)
        self.tile_frame.grid(row=1)
        self.tile_frame.grid(pady=10)

        for j in range(self.board.shape[1]):
            for i in range(self.board.shape[0]):
                subframe = Frame(self.tile_frame, borderwidth=1, relief="solid")
                subframe.grid(row=j, column=i, padx=1, pady=1)
                lbl = Label(subframe, text=self.board[i, j], width=10, height=5)
                lbl.grid(row=0)

                def click(event):
                    x, y = event.widget.master.grid_info()['row'], event.widget.master.grid_info()['column']
                    if self.board[x, y] is not None:
                        lstbox = Listbox(event.widget.master, relief="flat", width=10, height=4, bg="#F0F0F0", activestyle="none", highlightthickness=0, selectmode="single")
                        for k, lst in enumerate(get_values()):
                            lstbox.insert(k, lst)
                        lstbox.grid(row=0, padx=0, pady=0)
                        lstbox.see(get_values().index(event.widget.cget("text")))
                        lstbox.select_set(get_values().index(event.widget.cget("text")))
                        self.board[x, y] = None
                        lstbox.bind("<Button-3>", click)
                    else:

                        self.board[x, y] = event.widget.get(event.widget.curselection())
                        lbl = Label(event.widget.master, text=self.board[x, y], width=10, height=5)
                        lbl.grid(row=0)
                        lbl.bind("<Button-3>", click)

                lbl.bind("<Button-3>", click)

    def get_filename(self):
        self.filename = fd.askopenfilename(initialdir=os.getcwd(), )

    def open_file(self):
        self.get_filename()
        if self.filename:
            self.board = np.loadtxt(self.filename, delimiter=",", dtype=str)
            print(self.board)
            self.load_board()
            self.filemenu.entryconfig("Save", state="normal")
            self.filemenu.entryconfig("Save As...", state="normal")

    def save_file(self):
        if self.filename:
            np.savetxt(self.filename, self.board, delimiter=",", fmt='%s')

    def save_as_file(self):
        self.filename = fd.asksaveasfilename(initialdir=os.getcwd(), title="Select file to save level to",
                                             filetypes=[("Text Files", "*.txt")])
        np.savetxt(self.filename, self.board, delimiter=",", fmt='%s')
        self.filemenu.entryconfig("Save", state="normal")


def editor():
    ed = Tk()
    Editor(ed)
    ed.mainloop()


if __name__ == "__main__":
    editor()
