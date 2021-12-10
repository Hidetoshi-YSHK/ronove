import main
import tkinter as tk
import tkinterdnd2 as tkdnd

class Gui:
    def __init__(self, main:main.Main) -> None:
        self.main = main
        self.root = tkdnd.Tk()

    def mainloop(self) -> None:
        self.root.mainloop()
