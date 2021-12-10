from typing import Any 
import tkinter as tk
import tkinterdnd2 as tkdnd
import main

class Gui:
    def __init__(self, main:main.Main) -> None:
        self.main = main
        self.root = tkdnd.Tk()
        _LeftFrame(self.root).pack()
        _RightFrame(self.root).pack()

    def mainloop(self) -> None:
        self.root.mainloop()

class _LeftFrame(tk.Frame):
    def __init__(self, master: Any):
        super().__init__(master, bg="#ff0000")

    def pack(self) -> None:
        super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class _RightFrame(tk.Frame):
    def __init__(self, master: Any):
        super().__init__(master, bg="#00ff00")

    def pack(self) -> None:
        super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
