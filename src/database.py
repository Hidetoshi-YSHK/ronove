import sqlalchemy
from sqlalchemy.orm import sessionmaker
from english_word import EnglishWord
from sound import Sound
from image import Image
from orm_base import OrmBase

class Database:
    def __init__(self, filepath) -> None:
        print(filepath)
        self.engine = sqlalchemy.create_engine(
            self.get_connection_string(filepath))
        OrmBase.metadata.create_all(bind=self.engine)

    @classmethod
    def get_connection_string(cls, filepath) -> str:
        return f"sqlite:///{filepath}"
