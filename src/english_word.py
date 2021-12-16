from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
from sqlalchemy.orm import relationship
from orm_base import OrmBase

class EnglishWord(OrmBase):
    STATUS_UNPROCESSED = 0
    STATUS_PROCESSING = 1
    STATUS_PROCESSED = 2
    STATUS_ERROR = -1

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(length=256))
    status = Column(SmallInteger)
    pronunciation = Column(String(length=256))
    sound = relationship(
        "Sound",
        back_populates="english_word",
        uselist=False)
    image = relationship(
        "Image",
        back_populates="english_word",
        uselist=False)

    __tablename__ = "english_word"

    def __init__(self, word:str) -> None:
        super().__init__()
        self.id = None
        self.word = word
        self.status = EnglishWord.STATUS_UNPROCESSED
        self.pronunciation = ""
        self.sound = None
        self.image = None