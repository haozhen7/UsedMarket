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


# 댓글
class CreateComment(BaseModel):
    P_ID: int = Field(..., description="상품 ID")
    U_Name: str = Field(..., description="작성자 이름")
    P_Name: str = Field(..., description="상품 이름")
    P_UserName: str = Field(..., description="판매자 이름")
    Comments: str = Field(..., min_length=1, description="댓글 내용")

class CommentResponse(CreateComment):
    ID: int

    class Config:
        from_attributes = True

class UpdateComment(BaseModel): #댓글 수정
    Comments: str = Field(..., min_length=1, description="수정할 댓글 내용")
