from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, SQLModel

from data.config import macro_sett

# Create a database engine to connect with the database
engine = create_async_engine(
    url= macro_sett.POSTGRES_URL,
    #Log SQL queries
    echo = True
)

