from typing import Any, Literal, Optional 
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk

import ronove
import resources
import english_word
import singleton

class Gui(singleton.Singleton):
    WINDOW_MIN_WIDTH = 1280
    WINDOW_MIN_HEIGHT = 720
    BUTTON_WIDTH = 48
    BUTTON_HEIGHT = 48
    _GRID_UNIFORM_TOP = "grid_group_top"

    def initialize(self) -> None:
        self.table : Optional[_Table] = None

        self.root = tkdnd.Tk()
        self.root.geometry(f"{self.WINDOW_MIN_WIDTH}x{self.WINDOW_MIN_HEIGHT}")
        self.root.minsize(
            width=self.WINDOW_MIN_WIDTH, height=self.WINDOW_MIN_HEIGHT)
        _LeftFrame(self.root).deploy()
        _RightFrame(self.root).deploy()
        self.root.grid_columnconfigure(
            0, weight=12, uniform=self._GRID_UNIFORM_TOP)
        self.root.grid_columnconfigure(
            1, weight=4, uniform=self._GRID_UNIFORM_TOP)
        self.root.grid_rowconfigure(0, weight=1)

    def mainloop(self) -> None:
        self.root.mainloop()

    def refresh_table(
        self,
        english_words:list[english_word.EnglishWord]) -> None:
        if self.table is None:
            return
        self.table.delete(*self.table.get_children())
        for x in english_words:
            self.table.insert(
                "",
                tk.END,
                iid=str(x.id),
                values=(
                    x.id,
                    x.word,
                    self.get_status_string(x.status),
                    self.get_japanese_word_string(x.japanese_word),
                    x.pronunciation,
                    self.get_sound_string(x.sound_id),
                    self.get_image_string(x.image_id)
                )
            )

    def get_status_string(self, status:int) -> str:
        EnglishWord = english_word.EnglishWord
        status_string = {
            EnglishWord.STATUS_UNPROCESSED : "未処理",
            EnglishWord.STATUS_PROCESSING : "処理中",
            EnglishWord.STATUS_PROCESSED : "処理済",
            EnglishWord.STATUS_ERROR : "エラー",
            }
        return status_string[status]

    def get_japanese_word_string(self, japanese_word:str) -> str:
        return "" if japanese_word is None else japanese_word

    def get_sound_string(self, sound_id:int) -> str:
        return "なし" if sound_id is None else "あり"
        
    def get_image_string(self, image_id:int) -> str:
        return "なし" if image_id is None else "あり"


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
        self.download_button = _DownloadButton(self)

    def deploy(self) -> None:
        self.open_file_button.deploy()
        self.download_button.deploy()
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
        Gui.get_instance().table = self.table

    def deploy(self) -> None:
        self.scrollbar_h.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        self.scrollbar_v.pack(side=tk.RIGHT, anchor=tk.E, fill=tk.Y)
        self.table.deploy()
        super().pack(side=tk.TOP, anchor=tk.NW, fill=tk.BOTH, expand=True)

class _OpenFileButton(tk.Button):
    def __init__(self, master:Any) -> None:
        Resources = resources.Resources
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
        filetypes = [("英単語ファイル", "*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            answer = messagebox.askquestion(
                "読み込み設定",
                "既存の単語をスキップしますか？",
                icon=messagebox.INFO)
            skip_existing_word = (answer == messagebox.YES)
            rnv = ronove.Ronove.get_instance()
            rnv.load_english_word_file(filepath, skip_existing_word)

class _DownloadButton(tk.Button):
    def __init__(self, master:Any) -> None:
        Resources = resources.Resources
        self.image = Image.open(Resources.PROCESS_BUTTON.get_path())
        self.photo_image = ImageTk.PhotoImage(self.image)
        super().__init__(
            master,
            text="process",
            image=self.photo_image,
            compound=tk.TOP,
            width=Gui.BUTTON_WIDTH,
            height=Gui.BUTTON_HEIGHT,
            command=self.onclick)

    def deploy(self) -> None:
        super().pack(side=tk.LEFT)

    def onclick(self) -> None:
        pass

class _Table(ttk.Treeview):
    _COLUMN_ID = "id"
    _COLUMN_ENGLISH_WORD = "english_word"
    _COLUMN_STATUS = "status"
    _COLUMN_JAPANESE_WORD = "japanese_word"
    _COLUMN_PRONUNCIATION = "pronunciation"
    _COLUMN_SOUND = "sound"
    _COLUMN_IMAGE = "image"

    _COLUMNS = [
        _COLUMN_ID,
        _COLUMN_ENGLISH_WORD,
        _COLUMN_STATUS,
        _COLUMN_JAPANESE_WORD,
        _COLUMN_PRONUNCIATION,
        _COLUMN_SOUND,
        _COLUMN_IMAGE,
        ]

    _COLUMN_WIDTH = {
        _COLUMN_ID : 50,
        _COLUMN_ENGLISH_WORD : 200,
        _COLUMN_STATUS : 80,
        _COLUMN_JAPANESE_WORD : 300,
        _COLUMN_PRONUNCIATION : 200,
        _COLUMN_SOUND : 50,
        _COLUMN_IMAGE : 50,
    }

    _COLUMN_ANCHOR : dict[str, Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]] = {
        _COLUMN_ID : tk.CENTER,
        _COLUMN_ENGLISH_WORD : tk.W,
        _COLUMN_STATUS : tk.CENTER,
        _COLUMN_JAPANESE_WORD : tk.W,
        _COLUMN_PRONUNCIATION : tk.W,
        _COLUMN_SOUND : tk.CENTER,
        _COLUMN_IMAGE : tk.CENTER,
    }

    _COLUMN_HEADINGS = {
        _COLUMN_ID : "ID",
        _COLUMN_ENGLISH_WORD : "英単語",
        _COLUMN_STATUS : "状態",
        _COLUMN_JAPANESE_WORD : "日本語",
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
