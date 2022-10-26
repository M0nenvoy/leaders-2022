from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.session import SessionLocal, engine

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user (user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)


@app.post("/create-house/", response_model=schemas.HouseAddress)
def create_house (house: schemas.HouseAddressCreate, db: Session = Depends(get_db)):
    house_address = crud.create_house_address(db, house)
    # house_address = schemas.HouseAddress(address="Test address", id=1)
    return house_address


@app.get("/get-house/", response_model=int)
def get_house (address: str = "Not specified", db: Session = Depends(get_db)):
    return crud.get_house_id_by_address(db, address)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None: raise HTTPException(status_code=404, detail="User with id (%d) not found".format(user_id))
