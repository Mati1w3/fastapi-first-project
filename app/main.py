from typing import Optional, List  #  Type hints for optional values and lists (for older Python versions)
from fastapi import FastAPI, Response, status, HTTPException, Depends  #  Core FastAPI classes and tools for routes, responses, and dependencies
from pydantic import BaseModel  #  Data validation and serialization with Pydantic models
import psycopg2  #  PostgreSQL database adapter for Python
from psycopg2.extras import RealDictCursor  #  Fetches rows from PostgreSQL as dictionaries
import time  #  Used for sleep/retry logic (e.g. waiting for DB connection)
from sqlalchemy.orm import Session
from app.oauth2 import ALGORITHM  #  SQLAlchemy ORM session for database interactions
from . import models, schemas, utils   #  Local app modules for database models and Pydantic schemas
from .database import engine, get_db  #  Database engine and dependency for DB session
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

#engine = create_engine(SQLALCHEMY_DATABASE_URL)

#models.Base.metadata.create_all(bind=engine) - create tables

app = FastAPI()

""" 
uvicorn app.main:app --reload
model_dump - convert model to dict
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
#main page
@app.get("/") # decorators are used to add metadata to functions
def root():
    return {"message": "nigga"}