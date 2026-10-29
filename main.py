# 데코레이터, app, @get~ 실제 작동란
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from Database import get_db,engine
from Model import CreateTrade,ReadTrade,UpdateTrade #거래 신청, 조회, 수정(미승인->승인 같은?)
from schema import Trade_Requests,Base,Product
# from deps import CurrentUser

app=FastAPI()

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

@app.post('/trade',response_model=ReadTrade)
def create_trade(ct:CreateTrade,db:Session=Depends(get_db)): #current_user: CurrentUser,
    
    if db.query(Product).filter(Product.ID == ct.P_ID).first() is None:
        raise HTTPException(status_code=404, detail='상품이 없습니다.')
    
    create_trade=Trade_Requests(P_ID=ct.P_ID)#,U_name=current_user.username
    db.add(create_trade)
    db.commit()
    db.refresh(create_trade)

    return trade_view_query(db).filter(Trade_Requests.ID == create_trade.ID).first()

@app.get('/trade',response_model=list[ReadTrade])
def read_trade(#current_user:CurrentUser,
               P_status:bool=False,
               db:Session=Depends(get_db)):
    
    #q=trade_view_query(db).filter(Product.UserName == current_user.username)
    if P_status is not None:
        q=q.filter(Trade_Requests.P_status==P_status)
    return q.all()

@app.put('/trade/{trade_id}')
def update_trade(trade_id:int,ut:UpdateTrade,db:Session=Depends(get_db)):
    db_trade = db.query(Trade_Requests).filter(Trade_Requests.ID == trade_id).first()
    if db_trade is None:
        raise HTTPException(status_code=404, detail='거래신청이 없음')
    db_trade.P_status=ut.P_status
    db.commit()

    t=trade_view_query(db).filter(Trade_Requests.ID == trade_id).first()
    # if t.seller != current_user.username:
    #     raise HTTPException(status_code=403, detail='판매자만 승인할 수 있음')
    
    if t.P_status:
        msg = f"'{t.seller}'님의 상품 '{t.P_name}'을(를) '{t.buyer}'에게 판매하셨습니다."
    else:
        msg = f"'{t.seller}'님의 상품 '{t.P_name}'에 대한 '{t.buyer}'의 거래 승인이 취소되었습니다."
    
    return {"안내 메세지": msg}