from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, schemas
from database.session import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/create-house/", response_model=schemas.HouseAddress)
def create_house (house: schemas.HouseAddressCreate, db: Session = Depends(get_db)):
    # Сперва проверим, не существует ли уже дома с таким же адресом
    house_db = crud.get_house_address_by_address_str(db, address=house.address)
    if house_db:
        raise HTTPException(status_code=400, detail="House with this address already exists")

    return crud.create_house_address(db, house)


@app.post("/create-house-apartments/", response_model=schemas.HouseApartments)
def create_house_apartments(house: schemas.HouseApartmentsCreate, db: Session = Depends(get_db)):
    # Сперва проверим, не существует ли уже дома с таким же house_id
    house_apartments_db = crud.get_house_apartments_by_house_id(db, house.house_id)
    if house_apartments_db:
        raise HTTPException(status_code=400, detail="House with this house_id already exists")

    # Проверим, существует ли дом с id=house_id
    house_address_db = crud.get_house_address_by_id(db, house.house_id)
    if house_address_db is None:
        raise HTTPException(status_code=400, detail="No house with id={}. Can't reference with the foreign key".format(house.house_id))

    return crud.create_house_apartments(db, house)


@app.get("/get-house-apartments/{id}", response_model=schemas.HouseApartments)
def get_house_apartments(id: int, db: Session = Depends(get_db)):
    house_apartments = crud.get_house_apartments_by_house_id(db, id)
    if house_apartments is None:
        raise HTTPException(status_code=404, detail="House apartments with such id are not present")

    return house_apartments.__dict__


@app.get("/get-house/", response_model=int)
def get_house (address: str = "Not specified", db: Session = Depends(get_db)):
    import pdb; pdb.set_trace()
    house = crud.get_house_id_by_address(db, address)
    return house
