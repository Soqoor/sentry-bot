from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

# For mysql: mysql://<username>:<password>@<host>:<port>/<db>

# engine object that connects to the database specified.
engine = create_engine(settings.DATABASE_URL)

# create new session which is bound to the engine object created earlier.
# autocommit and autoflush false means not to make changes in database when there's
# change in session
LocalSession = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# Dependency
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
