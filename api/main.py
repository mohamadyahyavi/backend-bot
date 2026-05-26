from fastapi import FastAPI

from api.database import engine, Base
from api import models  # IMPORTANT: ensures models are loaded

# Import routers
from api.routes.auth import router as auth_router
from api.routes.products import router as products_router
from api.routes.orders import router as orders_router

app = FastAPI()


# -----------------------------
# DB Dependency (optional for later use)
# -----------------------------
from api.database import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    async with SessionLocal() as session:
        yield session


# -----------------------------
# Create tables on startup
# -----------------------------
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -----------------------------
# REGISTER ROUTES (THIS WAS MISSING)
# -----------------------------
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(orders_router)


# -----------------------------
# ROOT TEST ROUTE
# -----------------------------
@app.get("/")
async def root():
    return {"message": "API is running"}