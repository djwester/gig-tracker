from datetime import datetime

from sqlmodel import Field, SQLModel


class GigBase(SQLModel):
    date: datetime
    venue: str


class Gig(GigBase, table=True):
    id: int = Field(default=None, primary_key=True)


class GigCreate(GigBase):
    date: datetime


class GigPublic(GigBase):
    id: int


class Gigs(SQLModel):
    gigs: list[Gig]
