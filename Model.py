from pydantic import BaseModel, Field,ConfigDict

class CreateProduct(BaseModel):
    P_name:str=Field(...,min_length=1)
    Price:int=Field(...)
    UserName:str=Field('1')

class CreateCategories(BaseModel):
    C_Name:str=Field(...)

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