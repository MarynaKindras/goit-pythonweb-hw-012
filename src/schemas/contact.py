from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class ContactBase(BaseModel):
    first_name: str = Field(min_length=2, max_length=50,
                            description="Ім'я контакту")
    last_name: str = Field(min_length=2, max_length=50,
                           description="Прізвище контакту")
    email: EmailStr = Field(description="Електронна адреса")
    phone: str = Field(
        max_length=20,
        description="Номер телефону у форматі +380501234567",
        examples=["+380501234567"]
    )
    birthday: date = Field(description="Дата народження")
    additional_data: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Додаткова інформація"
    )

    @validator('birthday')
    def validate_birthday(cls, v):
        if v > date.today():
            raise ValueError("Дата народження не може бути в майбутньому")
        return v

    @validator('phone')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            v = '+' + v
        return v


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        None,
        max_length=20
    )
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True
