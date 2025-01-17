from datetime import date, time

from sqlmodel import Field, SQLModel


class GigBase(SQLModel):
    date: date
    time: time
    venue: str


class Gig(GigBase, table=True):
    id: int = Field(default=None, primary_key=True)


class GigCreate(GigBase): ...


class GigPublic(GigBase):
    id: int


class Gigs(SQLModel):
    gigs: list[Gig]
