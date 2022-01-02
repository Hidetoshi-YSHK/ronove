from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, SmallInteger, String, LargeBinary
from sqlalchemy.orm import relationship
from orm_base import OrmBase

class Image(OrmBase):
    EXTENSION_JPG = "jpg"
    EXTENSION_PNG = "png"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(LargeBinary)
    extension = Column(String)
    english_word = relationship(
        "EnglishWord",
        cascade="all, delete-orphan",
        back_populates="image",
        uselist=False)

    __tablename__ = "image"

    def __init__(self, data:bytes, extension:str) -> None:
        super().__init__()
        self.data = data
        self.extension = extension