import os
from typing import Union
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

    def select_all_english_words(self) -> list[english_word.EnglishWord]:
        session = self.Session()
        return session.query(english_word.EnglishWord).all()


