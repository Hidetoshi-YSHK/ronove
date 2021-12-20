import sys
import os
import os.path as path
from typing import Union
from database import Database
from english_word import EnglishWord
from singleton import Singleton

class Ronove(Singleton):
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
                    english_words.append(EnglishWord(word))

        database = Database.get_instance()
        database.add_english_words(english_words, skip_existing_word)
        self.on_english_words_change()

    def on_english_words_change(self) -> None:
        database = Database.get_instance()
        english_words = database.select_all_english_words()
        for english_word in english_words:
            print(vars(english_word))
