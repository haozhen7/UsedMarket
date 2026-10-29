"""SQLAlchemy ORM 모델 - 테이블 5개: users, categories, products, comments, trade_requests"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    """회원 - 컬럼 3개: user_id(PK), user_name(unique), password(해시된 값)"""
    __tablename__ = "users"

    user_id = Column(String(255), primary_key=True)
    user_name = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # 원문이 아니라 bcrypt 해시값이 저장됨


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String(500), nullable=True)
    # selling(판매 중) / sold(판매 완료)
    status = Column(String(20), default="selling", nullable=False, index=True)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    seller = relationship("User", lazy="joined")
    category = relationship("Category", lazy="joined")
    # 상품을 지우면 댓글·거래신청도 함께 삭제
    comments = relationship("Comment", back_populates="product", cascade="all, delete-orphan")
    trade_requests = relationship("TradeRequest", back_populates="product", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    author_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    product = relationship("Product", back_populates="comments")
    author = relationship("User", lazy="joined")


class TradeRequest(Base):
    __tablename__ = "trade_requests"
    # 한 사람이 한 상품에 신청 기록은 1개 (재신청하면 같은 행의 상태를 pending 으로 되돌림)
    __table_args__ = (
        UniqueConstraint("product_id", "buyer_id", name="uq_trade_request_product_buyer"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    buyer_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    # pending / accepted / rejected / cancelled / completed
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(DateTime, default=utcnow, nullable=False)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    product = relationship("Product", back_populates="trade_requests", lazy="joined")
    buyer = relationship("User", lazy="joined")
