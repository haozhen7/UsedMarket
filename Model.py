from pydantic import BaseModel, Field,ConfigDict,model_validator,EmailStr




class ORMModel(BaseModel):
    """ORM 객체를 그대로 응답으로 바꿀 수 있게 해주는 공통 설정"""
    model_config = ConfigDict(from_attributes=True)

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


###############회원/jwt###############

# ---------- Auth / Users ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    user_id: EmailStr
    password: str = Field(min_length=8, max_length=72)
    user_name: str = Field(min_length=1, max_length=50)


class UserUpdate(BaseModel):
    user_name: str = Field(min_length=1, max_length=50)


class UserPublic(ORMModel):
    """다른 사람에게 보여주는 정보: 이름만 (user_id 는 노출하지 않음)"""
    user_name: str


class UserRead(ORMModel):
    """내 정보: user_id 와 user_name (password 는 절대 포함하지 않음)"""
    user_id: EmailStr
    user_name: str