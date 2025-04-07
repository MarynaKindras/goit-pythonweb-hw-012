from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate
from src.services.auth import AuthService


class UserService:
    """
    Сервіс для роботи з користувачами.

    Attributes:
        db (AsyncSession): Сесія бази даних
        user_repository (UserRepository): Репозиторій користувачів
        auth_service (AuthService): Сервіс автентифікації
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(self.db)
        self.auth_service = AuthService(db)

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Створює нового користувача.

        Args:
            user_data (UserCreate): Дані для створення користувача

        Returns:
            User: Створений користувач
        """
        user = await self.auth_service.register_user(user_data)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Отримує користувача за іменем.

        Args:
            username (str): Ім'я користувача

        Returns:
            User | None: Користувач або None, якщо не знайдено
        """
        user = await self.user_repository.get_by_username(username)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Отримує користувача за email.

        Args:
            email (str): Email користувача

        Returns:
            User | None: Користувач або None, якщо не знайдено
        """
        user = await self.user_repository.get_user_by_email(email)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Підтверджує email користувача.

        Args:
            email (str): Email користувача

        Returns:
            None
        """
        user = await self.user_repository.confirmed_email(email)
        return user

    async def update_avatar_url(self, email: str, url: str):
        """
        Оновлює URL аватара користувача.

        Args:
            email (str): Email користувача
            url (str): Новий URL аватара

        Returns:
            None
        """
        return await self.user_repository.update_avatar_url(email, url)
