# db.py
from databases import Database
from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, text,
)
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import DuplicateDatabaseError
from sqlalchemy.exc import ProgrammingError
from datetime import datetime


from .config import settings, logger

database_url=settings.database_url
database = Database(database_url)
metadata = MetaData()

# Create a engine
engine = create_async_engine(
    settings.database_url,
    future=True,               # Use the new asyncio-based execution strategy
    pool_size=20,              # Adjust pool size based on your workload
    max_overflow=10,           # Adjust maximum overflow connections
    pool_recycle=3600,         # Periodically recycle connections (optional)
    pool_pre_ping=True,        # Check the connection status before using it
)

# Create database
async def create_database():
    db_uri = settings.database_url
    database_name = db_uri.split("/")[-1]
    uri_without_database = '/'.join(db_uri.split("/")[:-1])
    
    # Create a new engine without specifying a database
    engine = create_async_engine(
        uri_without_database,
        future=True,               # Use the new asyncio-based execution strategy
        pool_size=20,              # Adjust pool size based on your workload
        max_overflow=10,           # Adjust maximum overflow connections
        pool_recycle=3600,         # Periodically recycle connections (optional)
        pool_pre_ping=True,        # Check the connection status before using it
    )
    print('-------------------------------------------')
    # Create a new connection to execute the CREATE DATABASE statement
    try:
        async with engine.begin() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text(f"CREATE DATABASE {database_name}"))
            logger.info(f"Database '{database_name}' created successfully.")
    except (DuplicateDatabaseError, ProgrammingError):
        logger.warning(f"Database '{database_name}' already exists.")

# Create tables
async def create_tables():
    async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)

    # Print available tables
    table_names=list(metadata.tables.keys())
    logger.info(f"Tables created: {table_names}")

async def init_db():
    await create_database()
    await create_tables()
    await database.connect()

# Close database connection
async def close_db():
    await database.disconnect()