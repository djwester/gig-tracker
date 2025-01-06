from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel


class ClientBase(SQLModel):
    email_address: EmailStr
    first_name: str
    last_name: str
    phone_number: PhoneNumber
    address: str
    city: str
    province: str
    zip: str
    country: str


class Client(ClientBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # todo: Add relationship to gigs
    # todo: Add relationship to invoices
    # todo: Add communication log and relationship to it


class ClientCreate(ClientBase): ...


class ClientPublic(ClientBase):
    id: int
