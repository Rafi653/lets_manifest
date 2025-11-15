"""
Integration tests for database connectivity and connection pooling.
"""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine


@pytest.mark.asyncio
async def test_database_connection():
    """Test that we can connect to the database."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_database_version():
    """Test PostgreSQL version."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT version()"))
        version = result.scalar()
        assert "PostgreSQL" in version
        print(f"Database version: {version}")


@pytest.mark.asyncio
async def test_connection_pool():
    """Test connection pooling works correctly."""
    # Create multiple sessions to test pooling
    sessions = []
    for _ in range(3):
        session = AsyncSessionLocal()
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
        sessions.append(session)

    # Close all sessions
    for session in sessions:
        await session.close()


@pytest.mark.asyncio
async def test_transaction_rollback(db_session: AsyncSession):
    """Test that transactions can be rolled back."""
    from app.models.user import User

    # Create a user
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashedpassword",
    )
    db_session.add(user)
    await db_session.flush()

    # Verify user was added
    assert user.id is not None

    # Rollback the transaction
    await db_session.rollback()

    # Verify the session is still usable
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_transaction_commit(db_session_no_rollback: AsyncSession):
    """Test that transactions can be committed."""
    from app.models.user import User
    from sqlalchemy import select

    # Create a user
    user = User(
        email="commit@example.com",
        username="commituser",
        password_hash="hashedpassword",
    )
    db_session_no_rollback.add(user)
    await db_session_no_rollback.commit()

    # Verify user was committed
    result = await db_session_no_rollback.execute(select(User).where(User.email == "commit@example.com"))
    committed_user = result.scalar_one_or_none()
    assert committed_user is not None
    assert committed_user.email == "commit@example.com"


@pytest.mark.asyncio
async def test_pool_configuration():
    """Test that pool configuration is correct."""
    from app.core.config import settings

    assert engine.pool.size() == settings.DATABASE_POOL_SIZE
    assert engine.pool._max_overflow == settings.DATABASE_MAX_OVERFLOW


@pytest.mark.asyncio
async def test_uuid_extension():
    """Test that UUID extension is available."""
    async with AsyncSessionLocal() as session:
        # Test if uuid-ossp extension functions are available
        result = await session.execute(text("SELECT uuid_generate_v4()"))
        uuid_value = result.scalar()
        assert uuid_value is not None
        assert len(str(uuid_value)) == 36  # UUID format
