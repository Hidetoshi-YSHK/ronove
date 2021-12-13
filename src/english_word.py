from sqlalchemy import Column, Integer, SmallInteger, String, LargeBinary
from database import Database

class EnglishWord(Database.BaseClass):
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(length=256))
    status = Column(SmallInteger)
    pronunciation = Column(String(length=256))
    sound_data = Column(LargeBinary)
    image_data = Column(LargeBinary)

    __tablename__ = 'english_words'
