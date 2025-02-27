# SQLAlchemy models

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Float

from database.session import Base


"""
Модель, хранящая строку с адресом какого-либо дома
"""
class HouseAddress(Base):
    __tablename__ = "house_addresses"

    id      = Column(Integer, primary_key=True, index=True)
    address = Column(String)

    UniqueConstraint("address")


"""
Модель, хранящая число квартир в доме с идентификатором 'id' из модели HouseAdress
"""
class HouseApartments(Base):
    __tablename__ = "house_apartments"

    id          = Column(Integer, primary_key=True, index=True)
    apartments  = Column(Integer)
    house_id    = Column(Integer, ForeignKey("house_addresses.id"))

    UniqueConstraint("house_id")


"""
Модель, хранящая координаты дома в формате долготы и широты
"""
class HousePoint(Base):
    __tablename__ = "house_points"

    id          = Column(Integer, primary_key=True, index=True)
    house_id    = Column(Integer, ForeignKey("house_addresses.id"))
    lon         = Column(Float)
    lad         = Column(Float)

    UniqueConstraint("house_id")
