from datetime import date

from sqlmodel import Field, SQLModel


class Gig(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: date
    venue: str
    location: str
