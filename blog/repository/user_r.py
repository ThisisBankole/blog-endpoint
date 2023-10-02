from sqlalchemy.orm import Session
from .. import models, schemas
from ..hashing import Hash

def create(db: Session, request: schemas.UserCreate):
    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user
 