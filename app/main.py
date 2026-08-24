from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.database import engine, Base 
from app.models import User, Event, Ticket 
from app.routers import event, ticket, auth


@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  


app = FastAPI(
    lifespan=lifespan,
    title="Ticketing API"
)

app.include_router(event.router)
app.include_router(ticket.router)
app.include_router(auth.router)


@app.get("/", include_in_schema=False)
async def health_check():
    return {"status": "System Online and Connected to PostgreSQL"}


@app.get("/scalar", include_in_schema=False)
async def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Ticketing API"
    )
