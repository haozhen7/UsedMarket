from pydantic import BaseModel, Field,ConfigDict

class CreateProduct(BaseModel):
    P_name:str=Field(...,min_length=1)
    Price:int=Field(...)
    UserName:str=Field('1')

class CreateCategories(BaseModel):
    C_Name:str=Field(...)

############################댓글#################################
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



############################거래#################################
class CreateTrade(BaseModel):
    P_ID:int=Field(...)

class UpdateTrade(BaseModel):
    P_status:bool

class ReadTrade(BaseModel):
    ID: int          
    seller: str      
    P_name: str      
    buyer: str       
    P_status: bool   
    
    class Config:
        from_attributes = True
