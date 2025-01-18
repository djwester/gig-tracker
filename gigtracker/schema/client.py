from typing import TYPE_CHECKING

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .gig import Gig

PhoneNumber.phone_format = "E164"


class ClientBase(SQLModel):
    email_address: EmailStr
    first_name: str
    last_name: str
    phone_number: str  # TODO: Change to PhoneNumber
    address: str
    city: str
    province: str
    zip: str
    country: str


class Client(ClientBase, table=True):
    id: int = Field(default=None, primary_key=True)

    gigs: list["Gig"] = Relationship(back_populates="client")
    # todo: Add relationship to invoices
    # todo: Add communication log and relationship to it


class ClientCreate(ClientBase): ...


class ClientPublic(ClientBase):
    id: int
