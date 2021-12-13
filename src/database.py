import sqlalchemy
from sqlalchemy import Column, Integer, SmallInteger, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    BaseClass = declarative_base()

    def __init__(self, filepath) -> None:
        print(filepath)
        self.engine = sqlalchemy.create_engine(
            self.get_connection_string(filepath))
        self.BaseClass.metadata.create_all(bind=self.engine)

    @classmethod
    def get_connection_string(cls, filepath) -> str:
        return f"sqlite:///{filepath}"
