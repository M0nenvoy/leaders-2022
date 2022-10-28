from pydantic import BaseModel

class Point(BaseModel):
    lad: float
    lon: float


class Item(BaseModel):
    address_name:   str
    full_name:      str
    id:             str
    name:           str
    point:          Point
    purpose_name:   str
    type:           str


class Result(BaseModel):
    items:  list[Item]
