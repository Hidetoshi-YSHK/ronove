from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
from sqlalchemy.orm import relationship
from orm_base import OrmBase

class EnglishWord(OrmBase):
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
