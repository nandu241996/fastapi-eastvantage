from typing import List

from fastapi import Depends, FastAPI, HTTPException
from markupsafe import string
from sqlalchemy.orm import Session

from address_book_app import crud, models, schemas
from address_book_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/addresses/", response_model=schemas.Address)
def create_address_for_user(
    user_id: int, address_obj: schemas.AddressCreate, db: Session = Depends(get_db)
):
    return crud.create_address_item(db, address_obj=address_obj, user_id=user_id)


@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_addresses(db, skip=skip, limit=limit)


@app.get("/addresses/{distance}/{latitude}/{longitude}/", response_model=List[schemas.Address])
def read_nearby_addresses(distance: int, latitude: str, longitude: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nearby_addresses = crud.get_nearby_addresses(
        db, distance=distance, latitude=latitude, longitude=longitude, skip=skip, limit=limit)
    return nearby_addresses


@app.delete("/address/delete/{address_id}/{user_id}/")
def delete_address(address_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.delete_address(db, address_id=address_id, user_id=user_id)


@app.put("/address/update/{address_id}/", response_model=schemas.Address)
def update_address_item(address_id: int, address_obj: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.update_address_item(db, address_id=address_id, address_obj=address_obj)
