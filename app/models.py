from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

postgresql_db_url = "postgresql+psycopg2://postgres:1234@localhost:5432/fastapi"
engine = create_engine(postgresql_db_url)

Base = declarative_base()

class SQLAlchemyPost(Base):
    __tablename__ = "sqlalchemypost"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary Key with auto-increment
    title = Column(String, nullable=False)                     # Title column, NOT NULL constraint
    content = Column(String, nullable=False)                   # Content column, NOT NULL constraint
    published = Column(Boolean, default=True)                  # Published column, defaults to True
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Created_at column, defaults to current timestamp


Base.metadata.create_all(engine)




