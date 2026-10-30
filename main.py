# 데코레이터, app, @get~ 실제 작동란
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from Database import get_db,engine
from Model import CreateTrade,ReadTrade,UpdateTrade #거래 신청, 조회, 수정(미승인->승인 같은?)
from schema import Trade_Requests,Base,Product
from routers_comments import router as comments_router
import auth
import users
from deps import CurrentUser  

app=FastAPI()

app.include_router(comments_router)   

Base.metadata.create_all(bind=engine) #여기로 옮기는 게 좋을듯 

def trade_view_query(db: Session): #거래 join 테이블
    return (
        db.query(
            Trade_Requests.ID.label("ID"),
            Product.UserName.label("seller"),
            Product.P_Name.label("P_name"),
            Trade_Requests.U_name.label("buyer"),
            Trade_Requests.P_status.label("P_status"),
        )
        .join(Product, Trade_Requests.P_ID == Product.ID)
    )

@app.post('/trade',tags=["Trade"])
def create_trade(ct:CreateTrade,current_user: CurrentUser,db:Session=Depends(get_db)): 
    
    if db.query(Product).filter(Product.ID == ct.P_ID).first() is None:
        raise HTTPException(status_code=404, detail='상품이 없습니다.')
    
    create_trade=Trade_Requests(P_ID=ct.P_ID,U_name=current_user.user_name)
    db.add(create_trade)
    db.commit()
    db.refresh(create_trade)

    db_trade=trade_view_query(db).filter(Trade_Requests.ID == create_trade.ID).first()
    return [{"판매자":db_trade.seller,"구매상품":db_trade.P_name,"구매요청자":db_trade.buyer}, "현재 승인 요청 중"]

@app.get('/trade',response_model=list[ReadTrade],tags=["Trade"])
def read_trade(current_user:CurrentUser,
               P_status: bool | None = None,
               db:Session=Depends(get_db)):
    
    q=trade_view_query(db).filter(Product.UserName == current_user.user_name)
    if P_status is not None:
        q=q.filter(Trade_Requests.P_status==P_status)
    return q.all()

@app.put('/trade/{trade_id}',tags=["Trade"])
def update_trade(trade_id:int,ut:UpdateTrade,current_user:CurrentUser,db:Session=Depends(get_db)):
    db_trade = db.query(Trade_Requests).filter(Trade_Requests.ID == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail='거래신청이 없음')
    db_trade.P_status=ut.P_status

    t=trade_view_query(db).filter(Trade_Requests.ID == trade_id).first()
    if t.seller != current_user.user_name:
        raise HTTPException(status_code=403, detail='판매자만 승인할 수 있음')
    db.commit()
    
    if t.P_status:
        msg = f"'{t.seller}'님의 상품 '{t.P_name}'을(를) '{t.buyer}'에게 판매하셨습니다."
    else:
        msg = f"'{t.seller}'님의 상품 '{t.P_name}'에 대한 '{t.buyer}'의 거래 승인이 취소되었습니다."
    
    return {"안내 메세지": msg}

#거래 삭제는 귀찮으니까 패스합니다 ㅈㅈ

app.include_router(auth.router)
app.include_router(users.router)