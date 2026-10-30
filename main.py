# 데코레이터, app, @get~ 실제 작동란
from fastapi import FastAPI
from routers_comments import router as comments_router

app=FastAPI()

app.include_router(comments_router)   