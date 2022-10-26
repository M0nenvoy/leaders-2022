# SQLAlchemy models

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, index=True)
    owner_id    = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


"""
Модель, хранящая строку с адресом какого-либо дома
"""
class HouseAddress(Base):
    __tablename__ = "house_adresses"

    id      = Column(Integer, primary_key=True, index=True)
    address = Column(String)


"""
Модель, хранящая число квартир в доме с идентификатором 'id' из модели HouseAdress
"""
class HouseApartments(Base):
    __tablename__ = "house_apartments"

    id          = Column(Integer, primary_key=True, index=True)
    apartments  = Column(Integer)
    house_id    = Column(Integer, ForeignKey("house_adresses.id"))
