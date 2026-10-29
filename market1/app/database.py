from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#db url설정
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/jw1"

#엔진 생성(sqlalchemy에서 db와 연결할 엔진 생성)
engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

#sqlalchemy orm의 부모클래스
Base=declarative_base()


#요청마다 db 세션을 하나 열고, 요청이 끝나면 닫는 함수 (Depends 로 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
