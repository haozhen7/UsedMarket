# 만든 테이블들 모음
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String ,Boolean,ForeignKey
from Database import engine

class Base(DeclarativeBase): 
    pass

class Product(Base):
    __tablename__='Products'
    ID=Column(Integer, primary_key=True)
    P_Name=Column(String(50), nullable=False)
    Price=Column(Integer,nullable=False)
    UserName=Column(String(50),nullable=False)

class Categories(Base):
    __tablename__='Categories'
    ID=Column(Integer,primary_key=True)
    P_ID=Column(Integer,nullable=False)
    C_Name=Column(String(50),nullable=False)

# 코멘트
class Comments(Base):
    __tablename__ = 'Comments'
    ID = Column(Integer, primary_key=True, index=True)
    P_ID = Column(Integer, nullable=False)          # 상품 ID (어떤 상품의 댓글인지)
    U_Name = Column(String(50), nullable=False)     # 댓글 단 사람 이름
    P_Name = Column(String(50), nullable=False)     # 상품 이름
    P_UserName = Column(String(50), nullable=False) # 판매자 이름
    Comments = Column(String(500), nullable=False)  # 댓글 내용


Base.metadata.create_all(bind=engine)

class Trade_Requests(Base):
    __tablename__='trade_requests'
    ID=Column(Integer,primary_key=True)
    P_ID=Column(Integer,ForeignKey('Products.ID'),nullable=False)
    # P_name=Column(String(50),nullable=False) #상품이름
    U_name=Column(String(50),nullable=False) #구매자
    P_status=Column(Boolean,nullable= False, default= False)

# Base.metadata.create_all(bind=engine) # 이거 그냥 메인으로 이동
