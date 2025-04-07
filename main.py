from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import get_db, sessionmanager
from src.routes import contacts, auth, users

scheduler = AsyncIOScheduler()


async def cleanup_expired_tokens():
    async with sessionmanager.session() as db:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=7)
        stmt = text(
            "DELETE FROM refresh_tokens WHERE expired_at < :now OR revoked_at IS NOT NULL AND revoked_at < :cutoff"
        )
        await db.execute(stmt, {"now": now, "cutoff": cutoff})
        await db.commit()
        print(
            f"Expired tokens cleaned up [{now.strftime('%Y-%m-%d %H:%M:%S')}]")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстний менеджер для життєвого циклу FastAPI додатку.

    Args:
        app (FastAPI): Екземпляр FastAPI додатку

    Yields:
        None: Після завершення роботи планувальника
    """
    scheduler.add_job(cleanup_expired_tokens, "interval", hours=1)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="Contacts Application ",
    description="Contacts Application",
    version="1.0",
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Обробник винятку перевищення ліміту запитів.

    Args:
        request (Request): Об'єкт запиту
        exc (RateLimitExceeded): Виняток перевищення ліміту

    Returns:
        JSONResponse: Відповідь з помилкою та статусом 429
    """
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Перевищено ліміт запитів. Спробуйте пізніше."},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
def read_root(request: Request):
    return {"message": "Contacts Application"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Ендпоінт для перевірки стану бази даних.

    Args:
        db (AsyncSession): Сесія бази даних

    Returns:
        dict: Повідомлення про успішне підключення

    Raises:
        HTTPException: Якщо база даних не налаштована або недоступна
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
