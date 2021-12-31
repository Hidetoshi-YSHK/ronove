import sys
import os
import os.path as path
import time
import csv
from typing import Union

import gui
import database
import english_word
import sound
import image
import singleton
import weblio_page
import eijirou_page

class Ronove(singleton.Singleton):
    DB_FILE_NAME = "data.db"
    CSV_FILE_NAME = "ronove.csv"
    CSV_FILE_ENCODING = "utf_8"
    MEDIA_DIR_NAME = "media"
    INTERVAL_SECONDS = 10
    PREFIX = "ronove"

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
        pronunciation = weblio.get_pronunciation()
        sound_file_data = weblio.get_sound_file_data()

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

    def export(self, directory_path:str) -> None:
        if not path.isdir(directory_path):
            os.makedirs(directory_path)
        self._export_media_files(directory_path)
        self._export_csv_file(directory_path)

    def _export_media_files(self, directory_path:str) -> None:
        media_dir_path = path.join(directory_path, self.MEDIA_DIR_NAME)
        if not path.isdir(media_dir_path):
            os.makedirs(media_dir_path)

        db = database.Database.get_instance()
        sounds = db.select_all_sounds()
        images = db.select_all_images()

        g = gui.Gui.get_instance()
        g.initialize_export_progress(len(sounds), len(images))

        for sound_i in sounds:
            self._export_sound_file(media_dir_path, sound_i)
            g.on_export_sound()

        for image_i in images:
            self._export_image_file(media_dir_path, image_i)
            g.on_export_image()

    def _export_sound_file(self, media_dir_path:str, snd:sound.Sound) -> None:
        sound_file_path = path.join(
            media_dir_path, self._get_sound_file_name(snd))
        with open(sound_file_path, "wb") as f:
            f.write(snd.data)

    def _export_image_file(self, media_dir_path:str, img:image.Image) -> None:
        image_file_path = path.join(
            media_dir_path, self._get_image_file_name(img))
        with open(image_file_path, "wb") as f:
            f.write(img.data)

    def _export_csv_file(self, directory_path:str) -> None:
        with open(
            path.join(directory_path, self.CSV_FILE_NAME),
            'w',
            encoding=self.CSV_FILE_ENCODING,
            newline="") as f:

            writer = csv.writer(f)
            db = database.Database.get_instance()
            english_words = db.select_all_english_words()
            for word_i in english_words:
                sound_column = ""
                snd = db.select_sound_of(word_i)
                if snd is not None:
                    sound_file_name = self._get_sound_file_name(snd)
                    sound_column = f"[sound:{sound_file_name}]"

                image_column = ""
                img = db.select_image_of(word_i)
                if img is not None:
                    image_file_name = self._get_image_file_name(img)
                    image_column = f"<img src='{image_file_name}'>"

                writer.writerow([
                    word_i.word,
                    word_i.pronunciation,
                    word_i.japanese_words,
                    sound_column,
                    image_column])

        g = gui.Gui.get_instance()
        g.on_export_csv()

    def _get_sound_file_name(self, snd:sound.Sound) -> str:
        return f"{self.PREFIX}{snd.id:08}.{snd.extension}"

    def _get_image_file_name(self, img:image.Image) -> str:
        return f"{self.PREFIX}{img.id:08}.{img.extension}"

    def on_app_start(self) -> None:
        self.on_english_words_change()
