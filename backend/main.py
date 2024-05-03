import random

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import parser
from crud import crud
from db import Base, engine, get_db
from schema import Quote

Base.metadata.create_all(engine)

app = FastAPI(
    title='Parser',
    openapi_url=f"/api/openapi.json"
)

@app.get("/randomquote")
async def get_random_qoute(db: Session = Depends(get_db)):
    max_id = crud.get_last_quote(db)
    random_id = random.randint(1, max_id.id)
    quote = crud.get_qoute_by_id(db, random_id)
    return Quote(
                id=quote.id_qoute,
                description=quote.quote,
                date=quote.date,
                )


@app.get("/lastquotes")
async def get_last_ten_quotes(
    db: Session = Depends(get_db)
):
    last_quotes = crud.get_ten_quotes(db)
    return [Quote(
                id=quote.id_qoute,
                description=quote.quote,
                date=quote.date,
                ) for quote in last_quotes]


@app.get("/parsing")
def add_qoutes(
        db: Session = Depends(get_db)
):
    url = parser.get_html()
    if parser.get_count_quotes(url) == crud.get_count(db):
        return
    elif crud.get_count(db) == 0:
        xml = parser.get_count_pages(url)
        quotes = parser.multithread(db, int(xml))
        return quotes
    else:
        return {"message": "Есть новые записи"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000)