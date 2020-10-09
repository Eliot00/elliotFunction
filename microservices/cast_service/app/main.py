from fastapi import FastAPI
from mangum import Mangum
from app.api.casts import casts
from app.api.db import metadata, database, engine

metadata.create_all(engine)

prefix = "/api/v1/casts"

app = FastAPI(openapi_prefix="/Demo", openapi_url=f"{prefix}/openapi.json", docs_url=f"{prefix}/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(casts, prefix=prefix, tags=['casts'])

handler = Mangum(app)