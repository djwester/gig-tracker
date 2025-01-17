from sqlmodel import Field, SQLModel


class VenueBase(SQLModel):
    name: str
    address: str
    city: str
    contact_number: str | None = None
    contact_email: str | None = None
    capacity: int | None = None
    notes: str | None = None


class Venue(VenueBase, table=True):
    id: int = Field(default=None, primary_key=True)


class VenueCreate(VenueBase): ...


class VenuePublic(VenueBase):
    id: int


class Venues(SQLModel):
    venues: list[Venue]
