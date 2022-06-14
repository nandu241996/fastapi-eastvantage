from sqlalchemy.orm import Session

from . import models, schemas
from .util import *
from fastapi import HTTPException


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()


def create_address_item(db: Session, address_obj: schemas.AddressCreate, user_id: int):
    db_item = models.Address(**address_obj.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_nearby_addresses(db: Session, distance: int, latitude: str, longitude: str, skip: int = 0, limit: int = 100):
    db_items = db.query(models.Address).offset(skip).limit(limit).all()
    required_addresses = filter_address_by_distance(
        db_items, distance, latitude, longitude)
    return required_addresses


def delete_address(db: Session, address_id: int, user_id: int):
    db_item = db.query(models.Address).filter(
        models.Address.id == address_id, models.Address.owner_id == user_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Deleted Successfully"}


def update_address_item(db: Session, address_id: int, address_obj: schemas.AddressCreate):
    db_item = db.query(models.Address).get(address_id)
    address_obj = address_obj.dict()
    # models.Address.id == address_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Address not found")
    db_item.address_line_1 = address_obj['address_line_1']
    db_item.address_line_2 = address_obj['address_line_2']
    db_item.state = address_obj['state']
    db_item.country = address_obj['country']
    db_item.latitude = address_obj['latitude']
    db_item.longitude = address_obj['longitude']
    db.commit()
    db.refresh(db_item)
    return db_item
