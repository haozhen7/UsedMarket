"""A. 인증 - 1번"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import security
import Model, schema
from deps import DbSession

router = APIRouter(tags=["Auth"])


@router.post("/auth/token", response_model=Model.Token, summary="로그인 · JWT 발급")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    # OAuth2 규격상 입력 칸 이름은 username 이지만, 여기에는 user_id 를 넣음
    user = db.get(schema.User, form.username.lower())  # user_id 가 PK 이므로 get 으로 바로 조회
    if user is None or not security.verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Model.Token(access_token=security.create_access_token(user.user_id))
