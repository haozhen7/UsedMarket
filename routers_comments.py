from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Database import get_db
from schema import Comments as CommentModel
from Model import CreateComment, CommentResponse, UpdateComment

router = APIRouter(tags=["Comments"])

# 1. 댓글 작성 (POST)
@router.post("/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment_in: CreateComment, db: Session = Depends(get_db)):
    db_comment = CommentModel(
        P_ID=comment_in.P_ID,
        U_Name=comment_in.U_Name,
        P_Name=comment_in.P_Name,
        P_UserName=comment_in.P_UserName,
        Comments=comment_in.Comments
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# 2. 특정 상품의 댓글 목록 조회 (GET) - 요청하신 포맷 반영
@router.get("/products/{p_id}/comments")
def get_product_comments(p_id: int, db: Session = Depends(get_db)):
    comments = db.query(CommentModel).filter(CommentModel.P_ID == p_id).all()
    
    result = []
    for c in comments:
        # 팀원분이 원하신 출력 형태 형식화
        formatted_text = f"[{c.P_Name} / {c.P_UserName}]\n - {c.U_Name} : {c.Comments}"
        result.append({
            "comment_id": c.ID,
            "display_format": formatted_text,
            "P_Name": c.P_Name,
            "P_UserName": c.P_UserName,
            "U_Name": c.U_Name,
            "Comments": c.Comments
        })
    return result

# 3. 댓글 수정 (PATCH)
@router.patch("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: int, comment_in: UpdateComment, db: Session = Depends(get_db)):
    # 수정할 댓글이 데이터베이스에 있는지 확인
    comment = db.query(CommentModel).filter(CommentModel.ID == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 댓글 내용 변경
    comment.Comments = comment_in.Comments
    db.commit()
    db.refresh(comment)
    return comment


# 4. 댓글 삭제 (DELETE)
@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    # 삭제할 댓글이 데이터베이스에 있는지 확인
    comment = db.query(CommentModel).filter(CommentModel.ID == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 댓글 삭제 수행
    db.delete(comment)
    db.commit()
    return None