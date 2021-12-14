from typing import Any, Literal 
import tkinter as tk
import tkinter.ttk as ttk
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk
from resources import Resources
from ronove import Ronove
from singleton import Singleton


class Gui(Singleton):
    WINDOW_MIN_WIDTH = 1280
    WINDOW_MIN_HEIGHT = 720
    BUTTON_WIDTH = 48
    BUTTON_HEIGHT = 48
    _GRID_UNIFORM_TOP = "grid_group_top"

    def __init__(self) -> None:
        self.root = tkdnd.Tk()
        self.root.geometry(f"{self.WINDOW_MIN_WIDTH}x{self.WINDOW_MIN_HEIGHT}")
        self.root.minsize(
            width=self.WINDOW_MIN_WIDTH, height=self.WINDOW_MIN_HEIGHT)

        _LeftFrame(self.root).deploy()
        _RightFrame(self.root).deploy()
        self.root.grid_columnconfigure(
            0, weight=9, uniform=self._GRID_UNIFORM_TOP)
        self.root.grid_columnconfigure(
            1, weight=7, uniform=self._GRID_UNIFORM_TOP)
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
    _BG_COLOR = "#808080"

    def __init__(self, master: Any) -> None:
        super().__init__(master, bg=self._BG_COLOR)
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
            height=Gui.BUTTON_HEIGHT,
            command=self.onclick)

    def deploy(self) -> None:
        super().pack(side=tk.LEFT)

    def onclick(self) -> None:
        Ronove.get_instance()
        pass

class _Table(ttk.Treeview):
    _COLUMN_ID = "id"
    _COLUMN_ENGLISH_WORD = "english_word"
    _COLUMN_STATUS = "status"
    _COLUMN_PRONUNCIATION = "pronunciation"
    _COLUMN_SOUND = "sound"
    _COLUMN_IMAGE = "image"

    _COLUMNS = [
        _COLUMN_ID,
        _COLUMN_ENGLISH_WORD,
        _COLUMN_STATUS,
        _COLUMN_PRONUNCIATION,
        _COLUMN_SOUND,
        _COLUMN_IMAGE,
        ]

    _COLUMN_WIDTH = {
        _COLUMN_ID : 80,
        _COLUMN_ENGLISH_WORD : 200,
        _COLUMN_STATUS : 80,
        _COLUMN_PRONUNCIATION : 200,
        _COLUMN_SOUND : 50,
        _COLUMN_IMAGE : 50,
    }

    _COLUMN_ANCHOR : dict[str, Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]] = {
        _COLUMN_ID : tk.CENTER,
        _COLUMN_ENGLISH_WORD : tk.CENTER,
        _COLUMN_STATUS : tk.CENTER,
        _COLUMN_PRONUNCIATION : tk.CENTER,
        _COLUMN_SOUND : tk.CENTER,
        _COLUMN_IMAGE : tk.CENTER,
    }

    _COLUMN_HEADINGS = {
        _COLUMN_ID : "ID",
        _COLUMN_ENGLISH_WORD : "英単語",
        _COLUMN_STATUS : "状態",
        _COLUMN_PRONUNCIATION : "発音",
        _COLUMN_SOUND : "音声",
        _COLUMN_IMAGE : "画像",
    }

    _SHOW_OPTION = "headings"

    def __init__(self, master: Any) -> None:
        super().__init__(master, columns=self._COLUMNS, show=self._SHOW_OPTION)
        for column in self._COLUMNS:
            self.column(
                column,
                width=self._COLUMN_WIDTH[column],
                anchor=self._COLUMN_ANCHOR[column])
            self.heading(
                column,
                text=self._COLUMN_HEADINGS[column],
                anchor=self._COLUMN_ANCHOR[column])


    def deploy(self) -> None:
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.Y, expand=True)
