import sys
import os
import os.path as path
from typing import Union

import gui;
import database;
import english_word;
import singleton;

class Ronove(singleton.Singleton):
    DB_FILE_NAME = "data.db"

    def __init__(self) -> None:
        super().__init__()

    def get_exe_dir(self) -> str:
        return path.dirname(path.abspath(sys.argv[0]))

    def get_db_file_path(self) -> str:
        return path.join(self.get_exe_dir(), Ronove.DB_FILE_NAME)

    def load_english_word_file(
        self,
        filepath:Union[str, bytes, os.PathLike],
        skip_existing_word:bool) -> None:

        english_words = []
        with open(filepath) as f:
            for word in f:
                word = word.strip()
                if word:
                    english_words.append(english_word.EnglishWord(word))

        db = database.Database.get_instance()
        db.add_english_words(english_words, skip_existing_word)
        self.on_english_words_change()

    def on_english_words_change(self) -> None:
        db = database.Database.get_instance()
        english_words = db.select_all_english_words()
        gui.Gui.get_instance().refresh_table(english_words)
