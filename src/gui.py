from typing import Any 
import tkinter as tk
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk
import main
from resources import Resources


class Gui:
    BUTTON_WIDTH = 48
    BUTTON_HEIGHT = 48

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
        self.button_frame = _ButtonFrame(self)

    def pack(self) -> None:
        self.button_frame.pack()
        super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class _RightFrame(tk.Frame):
    def __init__(self, master: Any):
        super().__init__(master, bg="#00ff00")

    def pack(self) -> None:
        super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class _ButtonFrame(tk.Frame):
    def __init__(self, master: Any):
        super().__init__(master)
        self.open_file_button = _OpenFileButton(self)

    def pack(self) -> None:
        self.open_file_button.pack()
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.X, expand=True)

class _OpenFileButton(tk.Button):
    def __init__(self, master: Any):
        self.image = Image.open(Resources.OPEN_FILE_BUTTON.get_path())
        self.photo_image = ImageTk.PhotoImage(self.image)
        super().__init__(
            master,
            text="open",
            image=self.photo_image,
            compound=tk.TOP,
            width=Gui.BUTTON_WIDTH,
            height=Gui.BUTTON_HEIGHT)

    def pack(self) -> None:
        super().pack(side=tk.LEFT)