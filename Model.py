from pydantic import BaseModel, Field

class CreateProduct(BaseModel):
    P_name:str=Field(...,min_length=1)
    Price:int=Field(...)
    UserName:str=Field('1')

class CreateCategories(BaseModel):
    C_Name:str=Field(...)

# 상품등록 / 검색 > products 
# - P_name
# - Price
# - UserName (UNIQUE)

# 카테고리 > Categories
# - P_ID
# - C_Name




# #pydantic 모델
# class UserCreate(BaseModel):
#     username:str=Field(...,min_length=2, max_length=20)
#     password:str=Field(...,min_length=4)
#     email:EmailStr

# class BookCreate(BaseModel):
#     title:str=Field(..., min_length=2,max_length=40)
#     author:str=Field(..., min_length=2, max_length=40)
#     page:int=Field(..., ge=1, le=10000)
