from sqlalchemy import create_engine
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

# set engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# define base class
Base = declarative_base()


# dependency to get database session
# this is responsible to talk to the database
# it will create a session every time a request is made and then close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
