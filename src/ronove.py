import sys
import os
import os.path as path
import time
from typing import Union

from sqlalchemy.sql.schema import Column

import gui
import database
import english_word
import sound
import singleton
import weblio_page
import eijirou_page

class Ronove(singleton.Singleton):
    DB_FILE_NAME = "data.db"
    INTERVAL_SECONDS = 10

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
        gui.Gui.get_instance().update_table(english_words)

    def on_one_english_word_change(self, word:english_word.EnglishWord) -> None:
        db = database.Database.get_instance()
        word_db = db.select_one_english_word(word)
        gui.Gui.get_instance().update_one_english_word(word_db)

    def process_english_words(self) -> None:
        EnglishWord = english_word.EnglishWord
        db = database.Database.get_instance()
        english_words = db.select_all_english_words()
        for word_i in english_words:
            if word_i.status == EnglishWord.STATUS_PROCESSED:
                continue

            word_i.status = EnglishWord.STATUS_PROCESSING
            db.update_english_word(word_i)
            self.on_one_english_word_change(word_i)

            self.process_one_english_word(word_i)
            db.update_english_word(word_i)
            self.on_one_english_word_change(word_i)

            time.sleep(self.INTERVAL_SECONDS)

    def process_one_english_word(self, word:english_word.EnglishWord) -> None:
        # Weblioからデータ取得
        weblio = weblio_page.WeblioPage(word.word)
        japanese_words = weblio.get_joined_japanese_words()
        print(japanese_words)
        pronunciation = weblio.get_pronunciation()
        print(pronunciation)
        sound_file_data = weblio.get_sound_file_data()
        if sound_file_data:
            print(len(sound_file_data))

        # 和訳が取得できなければエラー
        if not japanese_words:
            word.status = english_word.EnglishWord.STATUS_ERROR
            return
        word.japanese_words = japanese_words # type: ignore

        # 発音記号の取得に失敗したら英辞郎を試す
        if not pronunciation:
            eijirou = eijirou_page.EijirouPage(word.word)
            pronunciation = eijirou.get_pronunciation()
        word.pronunciation = pronunciation # type: ignore

        # 音声データを保存する
        if sound_file_data is not None:
            snd = sound.Sound(sound_file_data, sound.Sound.EXTENSION_MP3)
            db = database.Database.get_instance()
            word.sound_id = db.add_sound(snd) # type: ignore

        # 英単語データを更新
        word.status = english_word.EnglishWord.STATUS_PROCESSED
        db = database.Database.get_instance()
        db.update_english_word(word)

    def on_app_start(self) -> None:
        self.on_english_words_change()
