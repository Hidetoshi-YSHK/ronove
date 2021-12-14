from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
from sqlalchemy.orm import relationship
from orm_base import OrmBase

class Sound(OrmBase):
    EXTENSION_MP3 = "mp3"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(LargeBinary)
    extension = Column(String)
    english_word_id = Column(Integer, ForeignKey("english_word.id"))
    english_word = relationship(
        "EnglishWord",
        back_populates="sound",
        cascade="all, delete-orphan")

    __tablename__ = "sound"
