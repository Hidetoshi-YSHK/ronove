import os
from typing import Union
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from orm_base import OrmBase
from english_word import EnglishWord
from sound import Sound
from image import Image
from singleton import Singleton

class Database(Singleton):
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
        english_words:list[EnglishWord],
        skip_existing_word:bool
        ) -> None:

        session = self.Session()
        for english_word in english_words:
            record = (session.query(EnglishWord)
                .filter(EnglishWord.word == english_word.word)
                .first())
            if record != None and skip_existing_word:
                continue
            session.add(english_word)
        session.commit()

    def select_all_english_words(self) -> list[EnglishWord]:
        session = self.Session()
        return session.query(EnglishWord).all()


