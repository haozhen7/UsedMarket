"""Pydantic 스키마 (요청 Body / 응답 모델)"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

TradeStatus = Literal["pending", "accepted", "rejected", "cancelled", "completed"]
ProductStatus = Literal["selling", "sold"]


class ORMModel(BaseModel):
    """ORM 객체를 그대로 응답으로 바꿀 수 있게 해주는 공통 설정"""
    model_config = ConfigDict(from_attributes=True)


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


# ---------- Categories ----------
class CategoryRead(ORMModel):
    id: int
    name: str


# ---------- Products ----------
class ProductCreate(BaseModel):
    category_id: int
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=2000)
    price: int = Field(ge=0)
    image_url: str | None = Field(default=None, max_length=500)


class ProductUpdate(BaseModel):
    """모든 항목 선택 (보낸 항목만 수정)"""
    category_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=2000)
    price: int | None = Field(default=None, ge=0)
    image_url: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def reject_null_for_required_fields(self):
        # image_url 만 null 로 지울 수 있고, 나머지는 null 로 보내면 안 됨
        for name in ("category_id", "title", "description", "price"):
            if name in self.model_fields_set and getattr(self, name) is None:
                raise ValueError(f"{name} 값은 null 일 수 없습니다.")
        return self


class ProductRead(ORMModel):
    id: int
    category_id: int
    title: str
    description: str
    price: int
    image_url: str | None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    seller: UserPublic
    category: CategoryRead


class ProductBrief(ORMModel):
    id: int
    title: str
    price: int
    image_url: str | None
    status: ProductStatus


class ProductList(BaseModel):
    items: list[ProductRead]
    total: int
    offset: int
    limit: int


# ---------- Comments ----------
class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentRead(ORMModel):
    id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    author: UserPublic


# ---------- Trade requests ----------
class TradeRequestStatusUpdate(BaseModel):
    status: Literal["accepted", "rejected", "cancelled", "completed"]


class TradeRequestRead(ORMModel):
    id: int
    product_id: int
    status: TradeStatus
    created_at: datetime
    updated_at: datetime
    buyer: UserPublic
    product: ProductBrief
