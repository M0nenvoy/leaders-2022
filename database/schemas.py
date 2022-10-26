from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
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
    items: list[Item] = []

    class Config:
        orm_mode = True



class HouseAddressBase(BaseModel):
    address: str


class HouseAddressCreate(HouseAddressBase):
    pass


class HouseAddress(HouseAddressBase):
    id: int

    class Config:
        orm_mode = True


class HouseApartments(BaseModel):
    house_id: int
    apartments: int
