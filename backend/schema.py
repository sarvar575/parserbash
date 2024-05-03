from datetime import datetime

from pydantic import BaseModel

class Quote(BaseModel):
    id: int
    description: str
    date: datetime