from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, oauth2
from typing import List
from ..db import get_db
from sqlalchemy.orm import Session
from ..repository import blog_r

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"],
)


@router.get("/", response_model=list[schemas.ShowBlog])
async def get_all(db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    return blog_r.get_all(db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def get_one(id:int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id:int, request: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.update(request.model_dump())
    db.commit()
    return {"message": f"Blog with id {id} updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id:int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Blog with id {id} deleted successfully"}


