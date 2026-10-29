from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


hojin="mysql+mysqlconnector://root:Hodori1503!@127.0.0.1:3306/hj2"
#비동기 db연결 생성하는 함수(비동기적으로 db와 연결한다)
engine=create_engine(hojin)

SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

