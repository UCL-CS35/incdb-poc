from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from app.initializers import settings

engine = create_engine(
    'sqlite:///app.sqlite', convert_unicode=True,
    pool_recycle=3600)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))