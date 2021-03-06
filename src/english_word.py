from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
import sqlalchemy
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
    japanese_words = Column(String(length=256))
    pronunciation = Column(String(length=256))
    sound_id = Column(Integer, ForeignKey("sound.id"))
    image_id = Column(Integer, ForeignKey("image.id"))
    sound = relationship(
        "Sound",
        back_populates="english_word")
    image = relationship(
        "Image",
        back_populates="english_word")

    __tablename__ = "english_word"

    def __init__(self, word:str) -> None:
        super().__init__()
        self.word = word
        self.status = EnglishWord.STATUS_UNPROCESSED