from sqlalchemy.orm import Session
from .. import models, schemas

def get_all(db: Session):
    list_blogs = models.Blog
    blogs = db.query(list_blogs).all()
    return blogs


