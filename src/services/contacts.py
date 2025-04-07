from datetime import date, timedelta
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repositories.contacts import ContactRepository
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse


class ContactService:
    """
    Сервіс для роботи з контактами.

    Attributes:
        repository (ContactRepository): Репозиторій контактів
    """

    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, contact: ContactCreate, user: User) -> ContactResponse:
        """
        Створює новий контакт.

        Args:
            contact (ContactCreate): Дані для створення контакту
            user (User): Користувач, який створює контакт

        Returns:
            ContactResponse: Створений контакт
        """
        return await self.repository.create_contact(contact, user)

    async def get_contacts(
        self,
        limit: int = 10,
        offset: int = 0,
        user: User = None
    ) -> List[ContactResponse]:
        """
        Отримує список контактів з пагінацією.

        Args:
            limit (int): Кількість контактів на сторінку
            offset (int): Зміщення для пагінації
            user (User): Користувач, чиї контакти потрібно отримати

        Returns:
            List[ContactResponse]: Список контактів
        """
        return await self.repository.get_contacts(limit, offset, user)

    async def get_contact(self, contact_id: int, user: User) -> Optional[ContactResponse]:
        """
        Отримує контакт за ID.

        Args:
            contact_id (int): ID контакту
            user (User): Користувач, чий контакт потрібно отримати

        Returns:
            Optional[ContactResponse]: Контакт або None, якщо не знайдено
        """
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(
        self,
        contact_id: int,
        contact_update: ContactUpdate,
        user: User
    ) -> Optional[ContactResponse]:
        """
        Оновлює контакт.

        Args:
            contact_id (int): ID контакту
            contact_update (ContactUpdate): Дані для оновлення
            user (User): Користувач, чий контакт оновлюється

        Returns:
            Optional[ContactResponse]: Оновлений контакт або None, якщо не знайдено
        """
        return await self.repository.update_contact(contact_id, contact_update, user)

    async def delete_contact(self, contact_id: int, user: User) -> Optional[ContactResponse]:
        """
        Видаляє контакт.

        Args:
            contact_id (int): ID контакту
            user (User): Користувач, чий контакт видаляється

        Returns:
            Optional[ContactResponse]: Видалений контакт або None, якщо не знайдено
        """
        return await self.repository.remove_contact(contact_id, user)

    async def get_upcoming_birthdays(self, user: User) -> List[ContactResponse]:
        """
        Отримує контакти з майбутніми днями народження.

        Args:
            user (User): Користувач, чиї контакти перевіряються

        Returns:
            List[ContactResponse]: Список контактів з майбутніми днями народження
        """
        today = date.today()
        end_date = today + timedelta(days=7)
        return await self.repository.get_contacts_with_birthday_between(today, end_date, user)

    async def search_contacts(self, query: str, user: User) -> List[ContactResponse]:
        """
        Розширений пошук контактів з додатковою бізнес-логікою
        """
        contacts = await self.repository.search_contacts(query, user)
        # Тут можна додати додаткову логіку, наприклад:
        # - Сортування результатів за релевантністю
        # - Фільтрація результатів
        # - Обмеження кількості результатів
        return contacts

    async def get_birthday_contacts(self, days: int = 7) -> List[ContactResponse]:
        """
        Отримання контактів з днями народження на вказану кількість днів
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        return await self.repository.get_contacts_with_birthday_between(today, end_date)
