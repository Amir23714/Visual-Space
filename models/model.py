from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

ALCHEMY_URL = "sqlite:///test.db"

engine = create_engine(ALCHEMY_URL)

SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    with SessonLocal() as session:
        yield session


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, index=True, primary_key=True)

    username = Column(String, index=True)

    password = Column(String, index=True)

    email = Column(String, index=True, unique=True)

    isAdmin = Column(Boolean, index=True, default=False)