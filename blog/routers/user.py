from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models
from typing import List
from ..db import get_db
from sqlalchemy.orm import Session
from ..repository import user_r

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_r.create(db, request)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
async def get_one_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user
    