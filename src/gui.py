from typing import Any 
import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk
import main
from resources import Resources


class Gui:
    WINDOW_MIN_WIDTH = 640
    WINDOW_MIN_HEIGHT = 480
    BUTTON_WIDTH = 48
    BUTTON_HEIGHT = 48
    _GRID_UNIFORM_TOP = "grid_group_top"

    def __init__(self, main:main.Main) -> None:
        self.main = main
        self.root = tkdnd.Tk()
        self.root.geometry(f"{self.WINDOW_MIN_WIDTH}x{self.WINDOW_MIN_HEIGHT}")
        self.root.minsize(
            width=self.WINDOW_MIN_WIDTH, height=self.WINDOW_MIN_HEIGHT)

        _LeftFrame(self.root).deploy()
        _RightFrame(self.root).deploy()
        self.root.grid_columnconfigure(
            0, weight=1, uniform=self._GRID_UNIFORM_TOP)
        self.root.grid_columnconfigure(
            1, weight=1, uniform=self._GRID_UNIFORM_TOP)
        self.root.grid_rowconfigure(0, weight=1)

    def mainloop(self) -> None:
        self.root.mainloop()

class _LeftFrame(tk.Frame):
    def __init__(self, master: Any) -> None:
        super().__init__(master, bg="#ff0000")
        self.button_frame = _ButtonFrame(self)
        self.table_frame = _TableFrame(self)

    def deploy(self) -> None:
        self.button_frame.deploy()
        self.table_frame.deploy()
        super().grid(row=0, column=0, sticky=tk.NSEW)

class _RightFrame(tk.Frame):
    def __init__(self, master: Any) -> None:
        super().__init__(master, bg="#00ff00")

    def deploy(self) -> None:
        super().grid(row=0, column=1, sticky=tk.NSEW)

class _ButtonFrame(tk.Frame):
    def __init__(self, master: Any) -> None:
        super().__init__(master)
        self.open_file_button = _OpenFileButton(self)

    def deploy(self) -> None:
        self.open_file_button.deploy()
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

class _TableFrame(tk.Frame):
    def __init__(self, master: Any) -> None:
        super().__init__(master, bg="#0000ff")
        self.table = _Table(self)
        self.scrollbar_h = ttk.Scrollbar(
            self, orient = tk.HORIZONTAL, command=self.table.xview)
        self.scrollbar_v = ttk.Scrollbar(
            self, orient = tk.VERTICAL, command=self.table.yview)
        self.table.configure(xscrollcommand=self.scrollbar_h.set)
        self.table.configure(yscrollcommand=self.scrollbar_v.set)

    def deploy(self) -> None:
        self.scrollbar_h.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        self.scrollbar_v.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y)
        self.table.deploy()
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True)

class _OpenFileButton(tk.Button):
    def __init__(self, master: Any) -> None:
        self.image = Image.open(Resources.OPEN_FILE_BUTTON.get_path())
        self.photo_image = ImageTk.PhotoImage(self.image)
        super().__init__(
            master,
            text="open",
            image=self.photo_image,
            compound=tk.TOP,
            width=Gui.BUTTON_WIDTH,
            height=Gui.BUTTON_HEIGHT)

    def deploy(self) -> None:
        super().pack(side=tk.LEFT)

class _Table(ttk.Treeview):
    _COLUMNS = [
        "id",
        "english_word",
        "status",
        "pronunciation",
        "sound",
        "image"
        ]
    def __init__(self, master: Any) -> None:
        super().__init__(master, columns=self._COLUMNS)

    def deploy(self) -> None:
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.Y, expand=True)
