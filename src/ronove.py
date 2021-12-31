import sys
import os
import os.path as path
from typing import Union

import gui
import database
import english_word
import singleton
import weblio_page
import eijirou_page

class Ronove(singleton.Singleton):
    DB_FILE_NAME = "data.db"

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

    def process_english_words(self) -> None:
        EnglishWord = english_word.EnglishWord
        db = database.Database.get_instance()
        english_words = db.select_all_english_words()
        for word_i in english_words:
            if word_i.status == EnglishWord.STATUS_PROCESSED:
                continue

            word_i.status = EnglishWord.STATUS_PROCESSING
            db.update_english_word(word_i)
            self.on_english_words_change()

            self.process_englis_word(word_i)

            db.update_english_word(word_i)
            self.on_english_words_change()

    def process_englis_word(self, word:english_word.EnglishWord) -> None:
        pass

    def on_app_start(self) -> None:
        self.on_english_words_change()
