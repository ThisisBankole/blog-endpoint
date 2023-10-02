from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, token
from ..db import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
async def login(request: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {request.username} not found")
    #verify password
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid password")
    #generate jwt token and return
    access_token = token.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}