"""A. 회원 - 2~4번"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .. import models, schemas, security
from ..deps import CurrentUser, DbSession

router = APIRouter(tags=["Users"])


@router.post(
    "/users",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
)
def register(body: schemas.UserCreate, db: DbSession):
    user_id = body.user_id.lower()
    if db.get(models.User, user_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 가입된 아이디입니다.")
    if db.scalar(select(models.User).where(models.User.user_name == body.user_name)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이름입니다.")

    user = models.User(
        user_id=user_id,
        user_name=body.user_name,
        password=security.hash_password(body.password),  # 해시해서 저장
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # 동시에 같은 아이디/이름으로 가입한 경우
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 아이디 또는 이름입니다.")
    db.refresh(user)
    return user


@router.get("/users/me", response_model=schemas.UserRead, summary="내 정보 조회")
def read_me(current_user: CurrentUser):
    return current_user


@router.patch("/users/me", response_model=schemas.UserRead, summary="내 이름 수정")
def update_me(body: schemas.UserUpdate, db: DbSession, current_user: CurrentUser):
    taken = db.scalar(
        select(models.User).where(
            models.User.user_name == body.user_name,
            models.User.user_id != current_user.user_id,  # 내 현재 이름과 같은 건 허용
        )
    )
    if taken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이름입니다.")

    current_user.user_name = body.user_name
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 사용 중인 이름입니다.")
    db.refresh(current_user)
    return current_user
