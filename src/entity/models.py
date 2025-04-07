from datetime import date
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import (
    String,
    Date,
    DateTime,
    func,
    ForeignKey,
    Text,
    Boolean,
    Enum as SqlEnum,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """
    Базовий клас для всіх моделей SQLAlchemy.

    Надає базову функціональність для ORM моделей.
    """
    pass


class Contact(Base):
    """
    Модель контакту.

    Attributes:
        id (int): Унікальний ідентифікатор контакту
        first_name (str): Ім'я
        last_name (str): Прізвище
        email (str): Email
        phone (str): Телефон
        birthday (date): Дата народження
        additional_data (str): Додаткові дані
        created_at (datetime): Дата створення
        updated_at (datetime): Дата оновлення
        user_id (int): ID користувача
        user (User): Зв'язаний користувач
    """
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    birthday: Mapped[date] = mapped_column(Date)
    additional_data: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", back_populates="contacts")


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    """
    Модель користувача системи.

    Attributes:
        id (int): Унікальний ідентифікатор користувача
        email (str): Email користувача
        username (str): Ім'я користувача
        password (str): Хеш паролю
        created_at (datetime): Дата створення
        avatar (str): URL аватара
        refresh_token (str): Токен оновлення
        confirmed (bool): Статус підтвердження email
        contacts (List[Contact]): Список контактів користувача
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole), default=UserRole.USER, nullable=False
    )
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user"
    )
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact", back_populates="user", cascade="all, delete-orphan"
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )
    expired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(
        "User", back_populates="refresh_tokens")
