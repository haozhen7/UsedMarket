# 만든 테이블들 모음
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String 
from Database import engine
Base=DeclarativeBase()

# 상품등록 / 검색 > products 
# - ID (PK)
# - P_name
# - Price
# - UserName (UNIQUE)
# - 
# 카테고리 > Categories
# - ID
# - P_ID
# - C_Name

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