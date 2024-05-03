import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session

user = os.getenv('user', default='postgres')
password = os.getenv('pass', default='postgres')
host = os.getenv('host', default='localhost')
port = os.getenv('port', default=5432)
db = os.getenv('db', default='postgres')

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)


SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Quotes(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_qoute = Column(String)
    quote = Column(String)
    date = Column(DateTime)



