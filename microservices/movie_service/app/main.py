from fastapi import FastAPI
from mangum import Mangum

from app.api.movies import movies
from app.api.db import metadata, database, engine


metadata.create_all(engine)

prefix = "/api/v1/movies"

# TODO: openapi_prefix用于适配api gateway的stage
# fastapi已经不推荐使用，寻找替代方式
app = FastAPI(openapi_prefix="/Demo", openapi_url=f"{prefix}/openapi.json", docs_url=f"{prefix}/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(movies, prefix=prefix, tags=['movies'])

handler = Mangum(app)
