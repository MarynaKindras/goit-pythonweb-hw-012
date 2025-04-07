from datetime import date, timedelta
from typing import Optional, Union, List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_contact(self, contact: ContactCreate, user: User) -> Contact:
        db_contact = Contact(**contact.model_dump(), user_id=user.id)
        self.db.add(db_contact)
        await self.db.commit()
        await self.db.refresh(db_contact)
        return db_contact

    async def get_contacts(self, limit: int, offset: int, user: User) -> List[Contact]:
        stmt = (
            select(Contact)
            .filter_by(user_id=user.id)
            .offset(offset)
            .limit(limit)
        )
        contacts = await self.db.execute(stmt)
        return list(await contacts.scalars())

    async def get_contact_by_id(self, contact_id: int, user: User) -> Optional[Contact]:
        stmt = select(Contact).filter_by(id=contact_id, user_id=user.id)
        contact = await self.db.execute(stmt)
        return await contact.scalar_one_or_none()

    async def update_contact(
        self, contact_id: int, contact_update: ContactUpdate, user: User
    ) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in contact_update.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(self, query: str, user: User) -> List[Contact]:
        stmt = select(Contact).filter(
            Contact.user_id == user.id,
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%")
            )
        )
        contacts = await self.db.execute(stmt)
        return list(await contacts.scalars())

    async def get_contacts_with_birthday_between(
        self, start_date: date, end_date: date, user: User
    ) -> List[Contact]:
        """
        Отримання контактів з днями народження між вказаними датами
        """
        stmt = select(Contact).filter(
            Contact.user_id == user.id,
            Contact.birthday.between(start_date, end_date)
        )
        contacts = await self.db.execute(stmt)
        return list(await contacts.scalars())
