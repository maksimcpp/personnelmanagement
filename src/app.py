from contextlib import asynccontextmanager
from fastapi import FastAPI

from settings import settings
from infrastructure.databases.postgresql.session_manager import sessionmanager
from api.v1 import routers as api_v1

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(settings.database.get_database_url())

    try:
        yield

    finally:
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1.router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8000
    )
