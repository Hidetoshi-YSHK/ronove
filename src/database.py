import os
from typing import Union, Optional
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from orm_base import OrmBase

import english_word
import sound
import image
import singleton

class Database(singleton.Singleton):
    @classmethod
    def get_connection_string(cls, filepath) -> str:
        return f"sqlite:///{filepath}"

    def initialize(
        self,
        filepath:Union[str, bytes, os.PathLike]) -> None:

        self.engine = sqlalchemy.create_engine(
            self.get_connection_string(filepath))
        self.Session = sessionmaker(self.engine) 
        OrmBase.metadata.create_all(bind=self.engine)

    def add_english_words(
        self,
        english_words:list[english_word.EnglishWord],
        skip_existing_word:bool
        ) -> None:

        EnglishWord = english_word.EnglishWord
        session = self.Session()
        for word_i in english_words:
            record = (session.query(EnglishWord)
                .filter(EnglishWord.word == word_i.word)
                .first())
            if record != None and skip_existing_word:
                continue
            session.add(word_i)
        session.commit()
        session.close()

    def select_all_english_words(self) -> list[english_word.EnglishWord]:
        session = self.Session()
        english_words = session.query(english_word.EnglishWord).all()
        session.close()
        return english_words

    def select_one_english_word(
        self, word:english_word.EnglishWord) -> english_word.EnglishWord:
        session = self.Session()
        EnglishWord = english_word.EnglishWord
        record = (session.query(EnglishWord)
            .filter(EnglishWord.id == word.id)
            .one())
        session.close()
        if record.word != word.word:
            raise Exception("A word mismatch happened.")
        return record

    def update_english_word(self, word:english_word.EnglishWord) -> None:
        session = self.Session()
        try:
            EnglishWord = english_word.EnglishWord
            record = (session.query(EnglishWord)
                .filter(EnglishWord.id == word.id)
                .one())
            if record.word != word.word:
                raise Exception("A word mismatch happened.")
            record.status = word.status
            record.japanese_words = word.japanese_words
            record.pronunciation = word.pronunciation
            record.sound_id = word.sound_id
            record.image_id = word.image_id
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def add_sound(self, snd:sound.Sound) -> int:
        session = self.Session()
        session.add(snd)
        session.commit()
        session.refresh(snd)
        if snd.id is None:
            raise Exception("sound.id is None.")
        return snd.id

    def select_all_sounds(self) -> list[sound.Sound]:
        session = self.Session()
        records = session.query(sound.Sound).all()
        session.close()
        return records

    def select_sound_of(
        self, word:english_word.EnglishWord) -> Optional[sound.Sound]:
        if word.sound_id is None:
            return None
        Sound = sound.Sound
        session = self.Session()
        record = (session.query(Sound)
            .filter(Sound.id == word.sound_id)
            .first())
        session.close()
        return record

    def select_all_images(self) -> list[image.Image]:
        session = self.Session()
        records = session.query(image.Image).all()
        session.close()
        return records

    def select_image_of(
        self, word:english_word.EnglishWord) -> Optional[image.Image]:
        if word.image_id is None:
            return None
        Image = image.Image
        session = self.Session()
        record = (session.query(Image)
            .filter(Image.id == word.image_id)
            .first())
        session.close()
        return record