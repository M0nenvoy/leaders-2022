from sqlalchemy.orm import Session

from . import models, schemas


def create_house_address(db: Session, house: schemas.HouseAddressCreate):
    db_item = models.HouseAddress(address = house.address)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_house_id_by_address(db: Session, address: str):
    house = db.query(models.HouseAddress).filter(models.HouseAddress.address == address).first()
    if house is None:
        return -1

    return house.id


def get_house_address_by_address_str(db: Session, address: str):
    house = db.query(models.HouseAddress).filter(models.HouseAddress.address==address).first()
    return house


def get_house_address_by_id(db: Session, id: int):
    return db.query(models.HouseAddress).filter(models.HouseAddress.id==id).first()


def get_house_apartments_by_house_id(db: Session, house_id: int):
    return db.query(models.HouseApartments).filter(models.HouseApartments.house_id==house_id).first()


def create_house_apartments(db: Session, house: schemas.HouseApartmentsCreate):
    db_item = models.HouseApartments(**house.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
