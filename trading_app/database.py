from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from trading_app.config import settings

# set up database url
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

SQLALCHEMY_DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

# set engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# define base class
Base = declarative_base()

# set async engine
engine_async = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC, echo=True)
# create async session
SessionLocalAsync = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine_async)


# dependency to get database session
# this is responsible to talk to the database
# it will create a session every time a request is made and then close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_async():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
