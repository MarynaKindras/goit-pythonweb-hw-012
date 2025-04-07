from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, UserRole
from src.services.auth import AuthService, oauth2_scheme
from src.services.user import UserService


def get_auth_service(db: AsyncSession = Depends(get_db)):
    """
    Залежність для отримання сервісу автентифікації.

    Args:
        db (AsyncSession): Сесія бази даних

    Returns:
        AuthService: Сервіс автентифікації
    """
    return AuthService(db)


def get_user_service(db: AsyncSession = Depends(get_db)):
    """
    Залежність для отримання сервісу користувачів.

    Args:
        db (AsyncSession): Сесія бази даних

    Returns:
        UserService: Сервіс користувачів
    """
    return UserService(db)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Залежність для отримання поточного користувача.

    Args:
        token (str): JWT токен
        auth_service (AuthService): Сервіс автентифікації

    Returns:
        User: Поточний користувач

    Raises:
        HTTPException: Якщо токен недійсний
    """
    return await auth_service.get_current_user(token)


# Залежності для перевірки ролей


def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """
    Залежність для перевірки прав адміністратора.

    Args:
        current_user (User): Поточний користувач

    Returns:
        User: Користувач з правами адміністратора

    Raises:
        HTTPException: Якщо користувач не має прав адміністратора
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Недостатньо прав доступу")
    return current_user
