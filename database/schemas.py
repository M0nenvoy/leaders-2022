from pydantic import BaseModel

class HouseAddressBase(BaseModel):
    address: str


class HouseAddressCreate(HouseAddressBase):
    pass


class HouseAddress(HouseAddressBase):
    id: int

    class Config:
        orm_mode = True


class HouseApartmentsCreate(BaseModel):
    house_id: int
    apartments: int


class HouseApartments(HouseApartmentsCreate):
    id: int

    class Config:
        orm_mode = True


class HousePointCreate(BaseModel):
    house_id:   int
    lon:        float
    lad:        float


class HousePoint(HousePointCreate):
    id: int

    class Config:
        orm_mode = True
