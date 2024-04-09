from sqlalchemy.orm import Session
from sqlalchemy import select
import models, schemas


def user_create(db: Session, user_in: schemas.UserCreate):
    user_db = models.User(
        email=user_in.email, about=user_in.about, hashed_password=user_in.password
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def user_get(db: Session, limit: int, skip: int):
    query = select(models.User).limit(limit).offset(skip)
    return db.scalars(query).all()


def user_get_by_mail(db: Session, email: str):
    query = select(models.User).where(models.User.email == email)
    return db.scalars(query).first()


def item_create(db: Session, item_in: schemas.ItemCreate, owner: int):
    item_db = models.Item(**item_in.model_dump(), owner_id=owner)
    db.add(item_db)
    db.commit()
    db.refresh(item_db)
    return item_db


def item_get(db: Session, limit: int = 100, skip: int = 0):
    query = select(models.Item).limit(limit).offset(skip)
    return db.scalars(query).all()
