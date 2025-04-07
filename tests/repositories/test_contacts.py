import pytest
from datetime import date
from unittest.mock import AsyncMock, Mock

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.contacts import ContactRepository
from src.entity.models import Contact, User
from src.schemas.contact import ContactCreate, ContactUpdate


@pytest.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_user():
    return User(id=1, email="test@example.com")


@pytest.fixture
def mock_contact():
    return Contact(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        birthday=date(1990, 1, 1),
        user_id=1
    )


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, mock_user):
    # Arrange
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        birthday=date(1990, 1, 1)
    )
    mock_contact = Contact(
        id=1,
        first_name=contact_data.first_name,
        last_name=contact_data.last_name,
        email=contact_data.email,
        phone=contact_data.phone,
        birthday=contact_data.birthday,
        user_id=mock_user.id
    )

    async def mock_refresh(contact):
        return mock_contact

    mock_session.refresh.side_effect = mock_refresh

    # Act
    result = await contact_repository.create_contact(contact_data, mock_user)

    # Assert
    assert result.first_name == mock_contact.first_name
    assert result.last_name == mock_contact.last_name
    assert result.email == mock_contact.email
    assert result.user_id == mock_contact.user_id
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    limit = 10
    offset = 0
    mock_contacts = [mock_contact]
    mock_result = Mock()
    mock_result.scalars = AsyncMock()
    mock_result.scalars.return_value = mock_contacts
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Act
    result = await contact_repository.get_contacts(limit, offset, mock_user)

    # Assert
    assert result == mock_contacts
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    contact_id = 1
    mock_result = Mock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=mock_contact)
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Act
    result = await contact_repository.get_contact_by_id(contact_id, mock_user)

    # Assert
    assert result == mock_contact
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    contact_id = 1
    update_data = ContactUpdate(first_name="Jane")
    mock_result = Mock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=mock_contact)
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.refresh = AsyncMock()

    # Act
    result = await contact_repository.update_contact(contact_id, update_data, mock_user)

    # Assert
    assert result.first_name == "Jane"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    contact_id = 1
    mock_result = Mock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=mock_contact)
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    # Act
    result = await contact_repository.remove_contact(contact_id, mock_user)

    # Assert
    assert result == mock_contact
    mock_session.delete.assert_called_once_with(mock_contact)
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_search_contacts(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    query = "John"
    mock_contacts = [mock_contact]
    mock_result = Mock()
    mock_result.scalars = AsyncMock()
    mock_result.scalars.return_value = mock_contacts
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Act
    result = await contact_repository.search_contacts(query, mock_user)

    # Assert
    assert result == mock_contacts
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_contacts_with_birthday_between(contact_repository, mock_session, mock_user, mock_contact):
    # Arrange
    start_date = date(1990, 1, 1)
    end_date = date(1990, 12, 31)
    mock_contacts = [mock_contact]
    mock_result = Mock()
    mock_result.scalars = AsyncMock()
    mock_result.scalars.return_value = mock_contacts
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Act
    result = await contact_repository.get_contacts_with_birthday_between(start_date, end_date, mock_user)

    # Assert
    assert result == mock_contacts
    mock_session.execute.assert_called_once()
