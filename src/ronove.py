import sys
import os
import os.path as path
from typing import Union
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
        filepath:Union[str, bytes, os.PathLike]) -> None:

        english_words = []
        with open(filepath) as f:
            for word in f:
                word = word.strip()
                if word:
                    english_words.append(EnglishWord(word))

        self.add_english_words(english_words)

    def add_english_words(self, english_words:list[EnglishWord]) -> None:
        pass