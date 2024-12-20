from datetime import datetime

from sqlmodel import Field, SQLModel


class Gig(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date: datetime
    venue: str


class Gigs(SQLModel):
    gigs: list[Gig]
