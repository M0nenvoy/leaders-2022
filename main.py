from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, schemas
from database.session import SessionLocal

from GIS import schemas as GISschemas

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
    house = crud.get_house_id_by_address(db, address)
    return house


@app.get("/get-house-point/{house_id}", response_model=GISschemas.Point)
def get_house_point (house_id: int, db: Session = Depends(get_db)):
    house_point = crud.get_house_point_by_house_id(db, house_id)
    if house_point is None:
        raise HTTPException(status_code=404, detail="House point with such house_id does not exist")

    return house_point.__dict__


@app.post("/create-house-point", response_model=schemas.HousePoint)
def create_house_point (house_point: schemas.HousePointCreate, db: Session = Depends(get_db)):
    # Проверим, существует ли точка дома с таким же house_id
    db_point = crud.get_house_point_by_house_id(db, house_point.house_id)
    if db_point:
        raise HTTPException(status_code=400, detail="House point with such house_id is already present")

    # Убедимся, что существует адрес с id=house_id
    db_address = crud.get_house_address_by_id(db, house_point.house_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="House address with such id doesn't exist")

    # Если точки не существует, то мы можем смело создавать новую точку
    return crud.create_house_point(db, house_point)
