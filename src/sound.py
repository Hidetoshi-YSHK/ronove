from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
from sqlalchemy.orm import relationship
from orm_base import OrmBase

class Sound(OrmBase):
    EXTENSION_MP3 = "mp3"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(LargeBinary)
    extension = Column(String)
    english_word = relationship(
        "EnglishWord",
        cascade="all, delete-orphan",
        back_populates="sound",
        uselist=False)

    __tablename__ = "sound"

    def __init__(self, data:bytes, extension:str) -> None:
        super().__init__()
        self.data = data
        self.extension = extension
