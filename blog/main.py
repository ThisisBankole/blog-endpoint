from fastapi import FastAPI
from . import models
from .db import engine
from sqlalchemy.orm import Session
from . import schemas
from .routers import blog, user, auth



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)












