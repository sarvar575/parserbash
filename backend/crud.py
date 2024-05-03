from sqlalchemy import  select, desc
from sqlalchemy.orm import Session
from db import Quotes

class Crud:

    @staticmethod
    def get_ten_quotes(db: Session):
        query = db.execute(
            select(Quotes).order_by(desc(Quotes.date)).limit(10))
        return query.scalars().all()

    @staticmethod
    def get_last_quote(db: Session):
        query = db.execute(
            select(Quotes).order_by(desc(Quotes.id)).limit(1))
        return query.scalar()

    @staticmethod
    def add_qoutes(db: Session, id_qoute, quote, date):
        new_quote = Quotes(id_qoute=id_qoute, quote=quote, date=date)
        db.add(new_quote)
        return new_quote

    @staticmethod
    def get_qoute(db: Session, id):
        query = db.execute(
            select(Quotes).where(Quotes.id_qoute==id))
        return query.scalar()

    @staticmethod
    def get_qoute_by_id(db: Session, id):
        query = db.execute(
            select(Quotes).where(Quotes.id == id))
        return query.scalar()

crud = Crud()