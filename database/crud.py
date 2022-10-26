from sqlalchemy.orm import Session

from . import models, schemas

# Read a single user by email
def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

# Read a single user by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Create a new 'User' entry
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Create a new 'Item' entry
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

# Read multiple items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


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

def create_house_apartments(db: Session, house: schemas.HouseApartments, house_id: int):
    db_item = models.HouseApartments(**house.dict(), house_id=house_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
