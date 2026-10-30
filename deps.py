"""공통 의존성(DB 세션, 현재 로그인 사용자)과 조회 헬퍼"""
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import schema
from Database import get_db
import security

# Swagger UI 의 Authorize 버튼이 이 주소로 로그인함 (username 칸에 user_id 입력)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DbSession
) -> schema.User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 올바르지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        user_id = payload["sub"]
    except (jwt.PyJWTError, KeyError):
        raise unauthorized

    user = db.get(schema.User, user_id)
    if user is None:
        raise unauthorized
    return user


CurrentUser = Annotated[schema.User, Depends(get_current_user)]


def _get_or_404(db: Session, model, object_id: int, message: str):
    obj = db.get(model, object_id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    return obj


def get_product_or_404(db: Session, product_id: int) -> schema.Product:
    return _get_or_404(db, schema.Product, product_id, "상품을 찾을 수 없습니다.")


def get_comment_or_404(db: Session, comment_id: int) -> schema.Comments:
    return _get_or_404(db, schema.Comments, comment_id, "댓글을 찾을 수 없습니다.")


def get_trade_request_or_404(db: Session, request_id: int) -> schema.Trade_Requests:
    return _get_or_404(db, schema.Trade_Requests, request_id, "거래 신청을 찾을 수 없습니다.")
