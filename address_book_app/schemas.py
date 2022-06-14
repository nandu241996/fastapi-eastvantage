from typing import List

from pydantic import BaseModel


class AddressBase(BaseModel):
    address_line_1: str
    address_line_2: str
    state: str
    country: str
    latitude: str
    longitude: str


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    addresses: List[Address] = []

    class Config:
        orm_mode = True
