from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import Settings
from routes.events import event_router
from routes.users import users_router


@asynccontextmanager
async def lifespan(app):
    await settings.init_database()
    yield


app = FastAPI(lifespan=lifespan)

# 출처 등록
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

settings = Settings()
app.include_router(users_router, prefix='/users')
app.include_router(event_router, prefix='/events')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
