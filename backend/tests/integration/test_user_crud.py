"""
Integration tests for CRUD operations on User model.
"""

from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test creating a new user."""
    user = User(
        email="create@example.com",
        username="createuser",
        password_hash="hashedpassword123",
        first_name="Create",
        last_name="User",
        timezone="America/New_York",
    )

    db_session.add(user)
    await db_session.flush()

    assert user.id is not None
    assert user.email == "create@example.com"
    assert user.username == "createuser"
    assert user.created_at is not None
    assert user.is_active is True
    assert user.is_verified is False


@pytest.mark.asyncio
async def test_read_user(db_session: AsyncSession):
    """Test reading a user from the database."""
    # Create a user
    user = User(
        email="read@example.com",
        username="readuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()
    user_id = user.id

    # Read the user back
    result = await db_session.execute(select(User).where(User.id == user_id))
    retrieved_user = result.scalar_one()

    assert retrieved_user.id == user_id
    assert retrieved_user.email == "read@example.com"
    assert retrieved_user.username == "readuser"


@pytest.mark.asyncio
async def test_update_user(db_session: AsyncSession):
    """Test updating a user."""
    # Create a user
    user = User(
        email="update@example.com",
        username="updateuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Update the user
    user.first_name = "Updated"
    user.last_name = "Name"
    user.bio = "This is my updated bio"
    await db_session.flush()

    # Verify updates
    result = await db_session.execute(select(User).where(User.id == user.id))
    updated_user = result.scalar_one()

    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.bio == "This is my updated bio"
    assert updated_user.updated_at is not None


@pytest.mark.asyncio
async def test_delete_user(db_session: AsyncSession):
    """Test deleting a user."""
    # Create a user
    user = User(
        email="delete@example.com",
        username="deleteuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()
    user_id = user.id

    # Delete the user
    await db_session.delete(user)
    await db_session.flush()

    # Verify deletion
    result = await db_session.execute(select(User).where(User.id == user_id))
    deleted_user = result.scalar_one_or_none()

    assert deleted_user is None


@pytest.mark.asyncio
async def test_unique_email_constraint(db_session: AsyncSession):
    """Test that email uniqueness is enforced."""
    from sqlalchemy.exc import IntegrityError

    # Create first user
    user1 = User(
        email="unique@example.com",
        username="uniqueuser1",
        password_hash="hashedpassword",
    )
    db_session.add(user1)
    await db_session.flush()

    # Try to create second user with same email
    user2 = User(
        email="unique@example.com",
        username="uniqueuser2",
        password_hash="hashedpassword",
    )
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_unique_username_constraint(db_session: AsyncSession):
    """Test that username uniqueness is enforced."""
    from sqlalchemy.exc import IntegrityError

    # Create first user
    user1 = User(
        email="user1@example.com",
        username="sameusername",
        password_hash="hashedpassword",
    )
    db_session.add(user1)
    await db_session.flush()

    # Try to create second user with same username
    user2 = User(
        email="user2@example.com",
        username="sameusername",
        password_hash="hashedpassword",
    )
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_user_timestamps(db_session: AsyncSession):
    """Test that user timestamps are set correctly."""
    user = User(
        email="timestamp@example.com",
        username="timestampuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Check created_at
    assert user.created_at is not None
    assert isinstance(user.created_at, datetime)

    # Update user and check updated_at
    original_updated_at = user.updated_at
    user.first_name = "Updated"
    await db_session.flush()

    assert user.updated_at is not None
    if original_updated_at:
        assert user.updated_at >= original_updated_at


@pytest.mark.asyncio
async def test_user_default_values(db_session: AsyncSession):
    """Test that user default values are set correctly."""
    user = User(
        email="defaults@example.com",
        username="defaultsuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    assert user.timezone == "UTC"
    assert user.is_active is True
    assert user.is_verified is False
